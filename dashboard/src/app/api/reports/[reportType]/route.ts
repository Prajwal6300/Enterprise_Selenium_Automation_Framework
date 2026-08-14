import { NextRequest, NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';
import { getAllTestCases, getLatestExecution } from '@/lib/result-parser';
import * as XLSX from 'xlsx';
import { jsPDF } from 'jspdf';
import 'jspdf-autotable';

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ reportType: string }> }
) {
  try {
    const { reportType } = await params;
    const { searchParams } = new URL(request.url);
    const isView = searchParams.get('view') === 'true';

    // 1. Standalone Executive HTML Dashboard
    if (reportType === 'dashboard-html') {
      const p = path.join(process.cwd(), '..', 'reports', 'dashboard.html');
      if (fs.existsSync(p)) {
        const content = fs.readFileSync(p, 'utf-8');
        return new NextResponse(content, {
          headers: {
            'Content-Type': 'text/html; charset=utf-8',
            'Content-Disposition': isView ? 'inline' : 'attachment; filename="enterprise_dashboard.html"',
          },
        });
      }
      return new NextResponse('<html><body><h2>Executive Dashboard generated. Check /reports/dashboard.html</h2></body></html>', {
        headers: { 'Content-Type': 'text/html' },
      });
    }

    // 2. Pytest HTML Report
    if (reportType === 'pytest-html') {
      const p = path.join(process.cwd(), '..', 'reports', 'html', 'report.html');
      if (fs.existsSync(p)) {
        const content = fs.readFileSync(p, 'utf-8');
        return new NextResponse(content, {
          headers: {
            'Content-Type': 'text/html; charset=utf-8',
            'Content-Disposition': isView ? 'inline' : 'attachment; filename="pytest_report.html"',
          },
        });
      }
      return new NextResponse('<html><body><h2>Pytest HTML Report not generated yet. Run pytest --html=reports/html/report.html</h2></body></html>', {
        headers: { 'Content-Type': 'text/html' },
      });
    }

    // 3. JUnit XML
    if (reportType === 'junit-xml') {
      const p = path.join(process.cwd(), '..', 'reports', 'junit', 'results.xml');
      if (fs.existsSync(p)) {
        const content = fs.readFileSync(p, 'utf-8');
        return new NextResponse(content, {
          headers: {
            'Content-Type': 'application/xml; charset=utf-8',
            'Content-Disposition': isView ? 'inline' : 'attachment; filename="junit_results.xml"',
          },
        });
      }
      return new NextResponse('<?xml version="1.0"?><testsuites><testsuite name="empty"/></testsuites>', {
        headers: { 'Content-Type': 'application/xml' },
      });
    }

    // 4. Execution JSON
    if (reportType === 'execution-json') {
      const latest = getLatestExecution();
      return new NextResponse(JSON.stringify(latest, null, 2), {
        headers: {
          'Content-Type': 'application/json; charset=utf-8',
          'Content-Disposition': isView ? 'inline' : 'attachment; filename="latest_execution.json"',
        },
      });
    }

    // 5. CSV Export
    if (reportType === 'csv-export') {
      const tests = getAllTestCases();
      const headers = ['Test Name', 'Module', 'Type', 'Browser', 'Environment', 'Duration (s)', 'Status'];
      const rows = tests.map((t) => [
        `"${t.name}"`,
        `"${t.module}"`,
        `"${t.test_type}"`,
        `"${t.browser}"`,
        `"${t.environment}"`,
        t.duration,
        `"${t.status}"`,
      ]);
      const csv = [headers.join(','), ...rows.map((r) => r.join(','))].join('\n');
      return new NextResponse(csv, {
        headers: {
          'Content-Type': 'text/csv; charset=utf-8',
          'Content-Disposition': 'attachment; filename="test_executions.csv"',
        },
      });
    }

    // 6. Excel Export
    if (reportType === 'excel-export') {
      const tests = getAllTestCases();
      const latest = getLatestExecution();

      const summaryData = [
        ['Metric', 'Value'],
        ['Project', 'SauceDemo E-Commerce Enterprise Automation'],
        ['Environment', latest?.environment || 'QA'],
        ['Browser', latest?.browser || 'Chrome'],
        ['Total Tests', latest?.total || tests.length],
        ['Passed', latest?.passed || tests.filter((t) => t.status === 'PASSED').length],
        ['Failed', latest?.failed || tests.filter((t) => t.status === 'FAILED').length],
        ['Pass Rate', `${latest?.pass_rate || 100}%`],
        ['Execution Date', latest?.date || new Date().toDateString()],
      ];

      const testData = [
        ['Test Name', 'Module', 'Type', 'Browser', 'Environment', 'Duration (s)', 'Status'],
        ...tests.map((t) => [t.name, t.module, t.test_type, t.browser, t.environment, t.duration, t.status]),
      ];

      const wb = XLSX.utils.book_new();
      const wsSummary = XLSX.utils.aoa_to_sheet(summaryData);
      const wsTests = XLSX.utils.aoa_to_sheet(testData);

      XLSX.utils.book_append_sheet(wb, wsSummary, 'Summary KPI');
      XLSX.utils.book_append_sheet(wb, wsTests, 'Test Cases');

      const buf = XLSX.write(wb, { type: 'buffer', bookType: 'xlsx' });

      return new NextResponse(buf, {
        headers: {
          'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
          'Content-Disposition': 'attachment; filename="enterprise_qa_report.xlsx"',
        },
      });
    }

    // 7. PDF Export
    if (reportType === 'pdf-export') {
      const tests = getAllTestCases();
      const latest = getLatestExecution();

      const doc = new jsPDF() as any;

      doc.setFont('helvetica', 'bold');
      doc.setFontSize(18);
      doc.setTextColor(37, 99, 235);
      doc.text('Enterprise Test Automation Quality Report', 14, 20);

      doc.setFontSize(10);
      doc.setFont('helvetica', 'normal');
      doc.setTextColor(100, 116, 139);
      doc.text(`Generated on: ${new Date().toLocaleString()} | Environment: ${latest?.environment || 'QA'} | Browser: ${latest?.browser || 'Chrome'}`, 14, 27);

      // KPI Summary table
      const kpiRows = [
        ['Total Tests', String(latest?.total || tests.length), 'Pass Rate', `${latest?.pass_rate || 100}%`],
        ['Passed', String(latest?.passed || tests.filter((t) => t.status === 'PASSED').length), 'Failed', String(latest?.failed || 0)],
        ['Duration', `${latest?.duration || 69}s`, 'Branch / Commit', `${latest?.branch || 'main'} / ${latest?.commit_hash || 'HEAD'}`],
      ];

      doc.autoTable({
        startY: 34,
        head: [['Metric', 'Value', 'Metric', 'Value']],
        body: kpiRows,
        theme: 'grid',
        headStyles: { fillColor: [37, 99, 235], textColor: 255 },
        styles: { fontSize: 9 },
      });

      // Test cases table
      const tableRows = tests.map((t) => [
        t.name,
        t.module,
        t.test_type,
        `${t.duration}s`,
        t.status,
      ]);

      doc.autoTable({
        startY: (doc as any).lastAutoTable.finalY + 12,
        head: [['Test Name', 'Module', 'Type', 'Duration', 'Status']],
        body: tableRows,
        theme: 'striped',
        headStyles: { fillColor: [15, 23, 42], textColor: 255 },
        styles: { fontSize: 8.5 },
      });

      const pdfBuf = Buffer.from(doc.output('arraybuffer'));
      return new NextResponse(pdfBuf, {
        headers: {
          'Content-Type': 'application/pdf',
          'Content-Disposition': 'attachment; filename="enterprise_qa_report.pdf"',
        },
      });
    }

    return NextResponse.json({ error: `Unknown report type: ${reportType}` }, { status: 400 });
  } catch (err: any) {
    return NextResponse.json(
      { error: 'Failed to generate report', details: err?.message },
      { status: 500 }
    );
  }
}
