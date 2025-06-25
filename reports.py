import pandas as pd
from fpdf import FPDF
import os
from database import engine
import numpy as np

def generate_report(subject_name):
    try:
        # Create reports directory
        os.makedirs('reports', exist_ok=True)
        
        # Get subject ID with type conversion
        subject_df = pd.read_sql(
            "SELECT id FROM subjects WHERE name = %s",
            engine,
            params=(subject_name,)
        )
        
        if subject_df.empty:
            print(f"No subject found: {subject_name}")
            return False
            
        # Convert numpy types to native Python
        subject_id = int(subject_df['id'].iloc[0].item()) if hasattr(subject_df['id'].iloc[0], 'item') else int(subject_df['id'].iloc[0])
        
        # Get attendance data with proper type handling
        query = """
        SELECT 
            s.roll_no as "Roll Number",
            s.name as "Student Name",
            DATE(a.date) as "Date",  # Ensures DATE format (YYYY-MM-DD)
            TIME(a.time) as "Time"   # Ensures TIME format (HH:MM:SS)
        FROM attendance a
        JOIN students s ON a.roll_no = s.roll_no
        WHERE a.subject_id = %s
        ORDER BY a.date, a.time
        """
        df = pd.read_sql(query, engine, params=(subject_id,))
        
        if df.empty:
            print(f"No records for {subject_name}")
            return False
        
        # Convert all numpy types to native Python
        for col in df.columns:
            if df[col].dtype == np.int64:
                df[col] = df[col].astype(int)
            elif df[col].dtype == np.float64:
                df[col] = df[col].astype(float)
        
        timestamp = pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')
        
        # Excel Report
        excel_path = f'reports/attendance_{subject_name}_{timestamp}.xlsx'
        with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
            
            workbook = writer.book
            worksheet = writer.sheets['Sheet1']
            
            # Format columns
            date_format = workbook.add_format({'num_format': 'yyyy-mm-dd'})
            time_format = workbook.add_format({'num_format': 'hh:mm:ss'})
            
            worksheet.set_column('C:C', 12, date_format)  # Date column
            worksheet.set_column('D:D', 12, time_format)  # Time column
        
        # PDF Report
        pdf_path = f'reports/attendance_{subject_name}_{timestamp}.pdf'
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, f'Attendance Report - {subject_name}', 0, 1, 'C')
        pdf.ln(10)
        
        # Table header
        col_widths = [30, 60, 30, 20]
        headers = df.columns
        pdf.set_font('Arial', 'B', 12)
        for i, header in enumerate(headers):
            pdf.cell(col_widths[i], 10, header, 1)
        pdf.ln()
        
        # Table rows
        pdf.set_font('Arial', '', 10)
        for _, row in df.iterrows():
            for i, col in enumerate(headers):
                pdf.cell(col_widths[i], 10, str(row[col]), 1)
            pdf.ln()
        
        pdf.output(pdf_path)
        
        print(f"Reports generated:\n- {excel_path}\n- {pdf_path}")
        return True
        
    except Exception as e:
        print(f"Report error: {str(e)}")
        return False