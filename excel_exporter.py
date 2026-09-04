# -*- coding: utf-8 -*-
"""
GitHub Daily Radar - Excel Exporter Module
Store and cumulatively update repository archive in an Excel spreadsheet (.xlsx).
"""

import os
from datetime import datetime
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def get_default_excel_path():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "reports", "github_radar_archive.xlsx")

def append_or_update_excel(categories_data, excel_path=None):
    """
    Append or update repository entries in the cumulative Excel database.
    """
    if excel_path is None:
        excel_path = get_default_excel_path()
        
    os.makedirs(os.path.dirname(excel_path), exist_ok=True)
    today_str = datetime.now().strftime("%Y-%m-%d")

    if os.path.exists(excel_path):
        try:
            wb = openpyxl.load_workbook(excel_path)
            ws = wb.active
        except Exception:
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "GitHub Radar Archive"
    else:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "GitHub Radar Archive"

    headers = [
        "Scan Date", 
        "Category", 
        "Repository", 
        "Stars", 
        "Forks", 
        "Velocity",
        "Language", 
        "Description", 
        "Use Case",
        "Tags / Topics", 
        "GitHub Link"
    ]

    if ws.max_row == 1 and ws.cell(row=1, column=1).value is None:
        ws.append(headers)
        header_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
        header_font = Font(name="Segoe UI", size=11, bold=True, color="FFFFFF")
        thin_border = Border(
            left=Side(style="thin", color="D9D9D9"),
            right=Side(style="thin", color="D9D9D9"),
            top=Side(style="thin", color="D9D9D9"),
            bottom=Side(style="thin", color="D9D9D9")
        )
        for col_num in range(1, len(headers) + 1):
            cell = ws.cell(row=1, column=col_num)
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.border = thin_border
        ws.row_dimensions[1].height = 28

    existing_repos = {}
    for row in range(2, ws.max_row + 1):
        repo_name = ws.cell(row=row, column=3).value
        if repo_name:
            existing_repos[repo_name.strip()] = row

    new_count = 0
    updated_count = 0

    body_font = Font(name="Segoe UI", size=10)
    link_font = Font(name="Segoe UI", size=10, color="0563C1", underline="single")
    alt_fill = PatternFill(start_color="F9FAFB", end_color="F9FAFB", fill_type="solid")

    for cat in categories_data:
        cat_name = cat["name"]
        for r in cat["repos"]:
            full_name = r["full_name"].strip()
            tags_str = ", ".join(r["topics"])
            velocity_str = r.get("velocity_badge", "Featured")
            use_case_str = r.get("ai_insight", {}).get("use_case", "AI Tooling")
            
            if full_name in existing_repos:
                row_idx = existing_repos[full_name]
                ws.cell(row=row_idx, column=1, value=today_str)
                ws.cell(row=row_idx, column=4, value=r["stars"])
                ws.cell(row=row_idx, column=5, value=r["forks"])
                ws.cell(row=row_idx, column=6, value=velocity_str)
                ws.cell(row=row_idx, column=8, value=r["description"])
                ws.cell(row=row_idx, column=9, value=use_case_str)
                updated_count += 1
            else:
                new_row = [
                    today_str,
                    cat_name,
                    full_name,
                    r["stars"],
                    r["forks"],
                    velocity_str,
                    r["language"],
                    r["description"],
                    use_case_str,
                    tags_str,
                    r["url"]
                ]
                ws.append(new_row)
                current_row = ws.max_row
                existing_repos[full_name] = current_row
                
                for c in range(1, len(new_row) + 1):
                    cell = ws.cell(row=current_row, column=c)
                    cell.font = body_font
                    if c in [1, 4, 5, 6, 7]:
                        cell.alignment = Alignment(horizontal="center", vertical="center")
                    else:
                        cell.alignment = Alignment(vertical="center")
                        
                    if current_row % 2 == 0:
                        cell.fill = alt_fill
                        
                link_cell = ws.cell(row=current_row, column=11)
                link_cell.hyperlink = r["url"]
                link_cell.font = link_font
                
                new_count += 1

    col_widths = {1: 14, 2: 32, 3: 28, 4: 12, 5: 12, 6: 18, 7: 15, 8: 50, 9: 35, 10: 30, 11: 40}
    for col_num, width in col_widths.items():
        ws.column_dimensions[get_column_letter(col_num)].width = width

    wb.save(excel_path)
    print(f"[+] Saved to Excel Archive: {excel_path} (+{new_count} new, {updated_count} updated, {len(existing_repos)} total repos)")
    return excel_path
