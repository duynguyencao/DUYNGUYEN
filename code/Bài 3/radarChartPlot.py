import pandas as pd  # Thêm thư viện pandas để đọc file CSV
import numpy as np
import matplotlib.pyplot as plt
import sys

def radar_chart(player1, player2, attributes, data1, data2):
    # Số lượng thuộc tính
    num_vars = len(attributes)

    # Tính toán góc cho mỗi trục
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

    # Hoàn thành vòng tròn
    data1 += data1[:1]  # Close the loop for data1
    data2 += data2[:1]  # Close the loop for data2
    angles += angles[:1]  # Close the loop for angles

    # Ensure data1 and data2 have the same length as angles
    if len(data1) != len(angles) or len(data2) != len(angles):
        raise ValueError("Data and angles must have the same length.")

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, data1, color='red', alpha=0.25)
    ax.fill(angles, data2, color='blue', alpha=0.25)
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(attributes)

    plt.title(f'Biểu đồ Radar: {player1} vs {player2}')
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) < 7:  # Check if there are enough arguments
        print("Usage: python radarChartPlot.py --p1 <player Name 1> --p2 <player Name 2> --Attribute <att1,att2,...,att_n>")
        sys.exit(1)

    player1 = sys.argv[2]  # Tên cầu thủ thứ nhất
    player2 = sys.argv[4]  # Tên cầu thủ thứ hai
    attributes = [attr.strip() for attr in sys.argv[6].split(',') if attr.strip()]  # Ensure no empty attributes
    print("Attributes:", attributes)  # Debugging line to check the attributes being passed
    # Ensure attributes are correctly parsed
    if len(attributes) == 0:
        raise ValueError("No valid attributes provided. Please check the input format.")

    # Đọc dữ liệu từ file CSV
    data = pd.read_csv(r'C:\baitaplon\result.csv')
    
    # Lấy dữ liệu cho hai cầu thủ
    data1 = data.loc[data['Player'] == player1, attributes].values.flatten().tolist()
    data2 = data.loc[data['Player'] == player2, attributes].values.flatten().tolist()

    radar_chart(player1, player2, attributes, data1, data2)

# python "C:\baitaplon\Bài 3\radarChartPlot.py" --p1 "Harry Maguire" --p2 "Erling Haaland" --Attribute "Non-Penalty Goals,Penalty Goals,Assists,PrgC"
