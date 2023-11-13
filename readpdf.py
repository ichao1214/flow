import pandas as pd
import camelot

pdf_file_path = "bank_statement.pdf"

# 从PDF文件提取表格数据
tables = camelot.read_pdf(pdf_file_path, pages='all', flavor='stream', row_tol=10)

# tables 变量包含提取的表格数据
col = ['Date', 'Currency', 'Transaction Amount', 'Balance', 'Transaction Type', 'Counter Party']

# 创建一个空的DataFrame来存储所有的表格数据
combined_df = pd.DataFrame(columns=col)

for table in tables:
    df = table.df
    df.columns = col
    df = df[df['Date'].str.match(r'\d{4}-\d{2}-\d{2}')]
    df = df.reset_index(drop=True)
    # 去掉字段中的换行符
    df['Transaction Type'] = df['Transaction Type'].str.replace('\n', ' ')
    df['Counter Party'] = df['Counter Party'].str.replace('\n', ' ')
    # 处理 "Transaction Amount" 和 "Balance" 字段，保留正负号并转换为数值
    df['Transaction Amount'] = df['Transaction Amount'].str.replace('[^\d.-]', '', regex=True).astype(float)
    df['Balance'] = df['Balance'].str.replace('[^\d.-]', '', regex=True).astype(float)
    # 将每个表格的数据追加到组合的DataFrame
    combined_df = pd.concat([combined_df, df], ignore_index=True)

print(combined_df)
combined_df.to_csv('flow.csv')
