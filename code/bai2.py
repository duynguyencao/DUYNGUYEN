import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns  # Thêm thư viện seaborn để tạo biểu đồ đẹp hơn
import numpy as np
import os  # Thêm import os để làm việc với thư mục

# Đọc file CSV và thay thế NaN bằng 0
file_path = r'C:\baitaplon\result.csv'
df = pd.read_csv(file_path, sep=',').fillna(0)

# Danh sách các chỉ số cần vẽ
expected_columns = [
    'Non-Penalty Goals', 'Penalty Goals', 'Assists', 'Matches Played',
    'Saves', 'Save%', 'Sh_x', 'SoTA',
    'Total Passes', 'Cmp%', 'xG', 'xAG',
    'Tkl', 'Int', 'Minutes', 'Starts_x',
    'Yellow Cards', 'Red Cards'
]

# Chuyển đổi kiểu dữ liệu cho các cột cần thiết thành số
df[expected_columns] = df[expected_columns].apply(pd.to_numeric, errors='coerce')

# Hàm tìm top 3 cầu thủ có điểm cao nhất và thấp nhất
def find_top_bottom_players(dataframe, columns):
    for column in columns:
        if column in dataframe.columns:
            top_players = dataframe.nlargest(3, column)[['Player', column]]
            bottom_players = dataframe.nsmallest(3, column)[['Player', column]]
            print(f"Top 3 cầu thủ có {column} cao nhất:\n{top_players}\n")
            print(f"Top 3 cầu thủ có {column} thấp nhất:\n{bottom_players}\n")

# Tìm top 3 cầu thủ cho từng chỉ số
find_top_bottom_players(df, expected_columns)

# Hàm vẽ histogram cho toàn giải và lưu thành ảnh PNG
def plot_histograms_overall(data, columns, output_dir):
    n_rows = (len(columns) // 3) + (len(columns) % 3 > 0)  # Số hàng cho subplot
    plt.figure(figsize=(18, 5 * n_rows))  # Tạo figure cho tất cả histogram
    
    for i, column in enumerate(columns, 1):
        plt.subplot(n_rows, 3, i)  # Tạo subplot cho từng chỉ số
        sns.histplot(data[column], bins=15, kde=True, color='skyblue', edgecolor='black', alpha=0.6)  # Điều chỉnh độ trong suốt
        plt.title(column, fontsize=20, fontweight='bold', pad=10)  # Tăng kích thước tiêu đề
        plt.xlabel(column, fontsize=14)
        plt.ylabel('Tần suất', fontsize=14)
        plt.grid(axis='y', alpha=0.5)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
    
    plt.tight_layout()
    plt.suptitle('Phân bố các chỉ số cho toàn giải', fontsize=28, fontweight='bold', y=1.02)
    plt.subplots_adjust(top=0.9, hspace=0.4, wspace=0.4)
    
    # Lưu hình ảnh với tên tương ứng
    plt.savefig(os.path.join(output_dir, 'overall_combined_histograms.png'), dpi=300)  # Lưu hình ảnh với độ phân giải cao
    plt.close()  # Đóng hình để giải phóng bộ nhớ

# Hàm vẽ histogram cho từng đội và lưu thành ảnh PNG
def plot_histograms_per_team(data, columns, team_name, output_dir):
    n_rows = (len(columns) // 3) + (len(columns) % 3 > 0)  # Số hàng cho subplot
    plt.figure(figsize=(18, 5 * n_rows))  # Tạo figure cho tất cả histogram
    
    for i, column in enumerate(columns, 1):
        plt.subplot(n_rows, 3, i)  # Tạo subplot cho từng chỉ số
        sns.histplot(data[column], bins=15, kde=True, color='lightgreen', edgecolor='black', alpha=0.6)  # Điều chỉnh độ trong suốt
        plt.title(f'{column} - {team_name}', fontsize=20, fontweight='bold', pad=10)  # Tăng kích thước tiêu đề
        plt.xlabel(column, fontsize=14)
        plt.ylabel('Tần suất', fontsize=14)
        plt.grid(axis='y', alpha=0.5)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
    
    plt.tight_layout()
    plt.suptitle(f'Phân bố các chỉ số cho đội {team_name}', fontsize=28, fontweight='bold', y=1.02)
    plt.subplots_adjust(top=0.9, hspace=0.4, wspace=0.4)
    
    # Lưu hình ảnh với tên tương ứng
    plt.savefig(os.path.join(output_dir, f'{team_name}_combined_histograms.png'), dpi=300)  # Lưu hình ảnh với độ phân giải cao
    plt.close()  # Đóng hình để giải phóng bộ nhớ

# Đường dẫn lưu hình ảnh
output_directory = r'C:\baitaplon\histograms'  # Thay đổi đường dẫn theo ý muốn

# Vẽ histogram cho toàn giải và lưu vào thư mục
plot_histograms_overall(df, expected_columns, output_directory)

# Vẽ histogram cho từng đội và lưu vào thư mục
for team in df['Team'].unique():
    team_data = df[df['Team'] == team]
    plot_histograms_per_team(team_data, expected_columns, team, output_directory)

# Hàm tính toán các thống kê và ghi vào file CSV
def calculate_statistics(dataframe, columns, output_file):
    results = []

    # Tính toán cho toàn bộ dữ liệu
    overall_stats = {'Team': 'all'}
    for col in columns:
        overall_stats[f'Median of {col}'] = dataframe[col].median()
        overall_stats[f'Mean of {col}'] = dataframe[col].mean()
        overall_stats[f'Std of {col}'] = dataframe[col].std()
    results.append(overall_stats)

    # Tính toán cho từng đội
    for team in dataframe['Team'].unique():
        team_data = dataframe[dataframe['Team'] == team]
        team_stats = {'Team': team}
        for col in columns:
            team_stats[f'Median of {col}'] = team_data[col].median()
            team_stats[f'Mean of {col}'] = team_data[col].mean()
            team_stats[f'Std of {col}'] = team_data[col].std()
        results.append(team_stats)

    # Ghi vào file CSV
    pd.DataFrame(results).to_csv(output_file, index=False)

# Gọi hàm để tính toán và ghi kết quả
calculate_statistics(df, expected_columns, r'C:\baitaplon\results2.csv')

# Hàm tìm đội bóng có chỉ số cao nhất cho mỗi chỉ số
def find_best_teams(dataframe, columns):
    best_teams = {}
    
    for column in columns:
        if column in dataframe.columns:
            # Tìm đội bóng có chỉ số cao nhất
            best_team = dataframe.loc[dataframe[column].idxmax(), 'Team']
            best_teams[column] = best_team
            
    return best_teams

# Tìm đội bóng có chỉ số cao nhất cho từng chỉ số
best_teams = find_best_teams(df, expected_columns)

# In ra kết quả
print("Đội bóng có chỉ số cao nhất cho mỗi chỉ số:")
for stat, team in best_teams.items():
    print(f"{stat}: {team}")

# Tính toán phong độ tốt nhất
# Giả sử phong độ tốt nhất được xác định bằng tổng điểm của các chỉ số
df['Total Score'] = df[expected_columns].sum(axis=1)
best_team_overall = df.loc[df['Total Score'].idxmax(), 'Team']

print(f"\nĐội bóng có phong độ tốt nhất giải Ngoại Hạng Anh mùa 2023-2024: {best_team_overall}")
