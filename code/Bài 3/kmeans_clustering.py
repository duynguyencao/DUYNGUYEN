import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Bước 1: Đọc dữ liệu từ file CSV
data = pd.read_csv(r'C:\baitaplon\result.csv')

# Bước 2: Tiền xử lý dữ liệu
features = data[['Age', 'Non-Penalty Goals', 'Penalty Goals','PrgP_x','PrgC','Assists']].dropna()  # Loại bỏ hàng có giá trị NaN
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)  # Chuẩn hóa dữ liệu

# Bước 3: Áp dụng KMeans
optimal_k = 3  # Thay đổi theo kết quả từ phương pháp Elbow
kmeans = KMeans(n_clusters=optimal_k, random_state=42)
clusters = kmeans.fit_predict(scaled_features)  # Gán nhãn cụm cho từng điểm dữ liệu
data.loc[features.index, 'Cluster'] = clusters  # Gán nhãn cụm cho các hàng tương ứng

# Bước 4: Áp dụng PCA để giảm số chiều xuống 2
pca = PCA(n_components=2)
pca_result = pca.fit_transform(scaled_features)  # Giảm số chiều dữ liệu
data.loc[features.index, 'PCA1'] = pca_result[:, 0]  # Thành phần chính 1
data.loc[features.index, 'PCA2'] = pca_result[:, 1]  # Thành phần chính 2

# Bước 5: Vẽ biểu đồ phân cụm
plt.figure(figsize=(10, 6))  # Thiết lập kích thước biểu đồ
scatter = plt.scatter(data['PCA1'], data['PCA2'], c=data['Cluster'], cmap='viridis', alpha=0.6)  # Vẽ biểu đồ phân tán
plt.title('PCA - K-means Clustering of Players (2D)')  # Tiêu đề biểu đồ
plt.xlabel('Principal Component 1')  # Nhãn trục x
plt.ylabel('Principal Component 2')  # Nhãn trục y
plt.colorbar(scatter, label='Cluster')  # Thêm thanh màu để hiển thị số cụm
plt.grid()  # Thêm lưới cho biểu đồ
plt.show()  # Hiển thị biểu đồ
