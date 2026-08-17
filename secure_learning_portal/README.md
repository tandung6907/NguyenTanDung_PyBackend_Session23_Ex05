# Secure Learning Portal

## 1. Mô tả sản phẩm

Secure Learning Portal là API quản lý tài nguyên học tập cho đơn vị đào tạo. Hệ thống tập trung vào xác thực JWT, phân quyền Admin/User, kiểm tra quyền sở hữu tài nguyên và hỗ trợ Frontend thông qua CORS.

## 2. Nỗi đau khách hàng

Đơn vị đào tạo cần kiểm soát người dùng truy cập hệ thống, biết ai đang thực hiện request, bảo vệ dữ liệu cá nhân và tài nguyên học tập, đồng thời cung cấp API dễ tích hợp với Frontend.

## 3. Nhóm người dùng

- Admin: quản lý người dùng và toàn bộ tài nguyên.
- User: đăng nhập, xem và quản lý tài nguyên thuộc quyền sở hữu của mình.

## 4. Chức năng

- Đăng ký tài khoản.
- Đăng nhập bằng email và mật khẩu.
- Tạo JWT.
- Lấy current user.
- Kiểm tra token hết hạn, token sai và token thiếu subject.
- Chặn tài khoản không hoạt động.
- Phân quyền Admin/User.
- Admin xem danh sách người dùng.
- Admin khóa người dùng.
- Admin xem toàn bộ tài nguyên.
- Admin xóa tài nguyên.
- User tạo, xem và cập nhật tài nguyên của mình.
- Kiểm tra quyền sở hữu tài nguyên.
- CORS.
- Request ID.
- Đo thời gian xử lý.
- Log method, URL và status code.
- Health check.

## 5. API

| Method | Endpoint | Quyền |
|---|---|---|
| POST | /auth/register | Public |
| POST | /auth/login | Public |
| GET | /auth/me | User/Admin |
| GET | /users/my-resources | User/Admin |
| GET | /resources | User/Admin |
| POST | /resources | User/Admin |
| GET | /resources/{resource_id} | Owner/Admin |
| PUT | /resources/{resource_id} | Owner/Admin |
| GET | /admin/users | Admin |
| PATCH | /admin/users/{user_id}/lock | Admin |
| GET | /admin/resources | Admin |
| DELETE | /admin/resources/{resource_id} | Admin |
| GET | /health | Public |

## 6. HTTP Status

- 400: dữ liệu nghiệp vụ không hợp lệ, ví dụ email đã tồn tại.
- 401: thiếu token, token sai, token hết hạn, user không tồn tại.
- 403: tài khoản bị khóa, sai role hoặc không sở hữu dữ liệu.
- 404: tài nguyên hoặc người dùng không tồn tại.
- 422: dữ liệu request sai kiểu hoặc thiếu trường bắt buộc.

## 7. Luồng kiến trúc

Frontend
↓
CORS Middleware
↓
Request Middleware
↓
Router
↓
Authentication Dependency
↓
Authorization Dependency
↓
Service
↓
SQLAlchemy
↓
SQLite/MySQL
↓
Response

## 8. Luồng JWT

Frontend gửi email và password đến POST /auth/login.

API tìm user và kiểm tra password.

Nếu hợp lệ, API tạo JWT có sub là user id và exp là thời điểm hết hạn.

Frontend gửi JWT trong header Authorization: Bearer <token>.

get_current_user giải mã JWT, kiểm tra exp, sub, user tồn tại và trạng thái tài khoản.

Nếu request cần quyền Admin, require_admin kiểm tra role.

## 9. Quyền sở hữu

User chỉ được GET hoặc PUT resource nếu resource.owner_id bằng current_user.id.

Nếu User truy cập resource của User khác, API trả về 403 Forbidden.

Admin có thể truy cập toàn bộ resource.

## 10. Middleware

RequestMiddleware tạo UUID cho mỗi request, đo thời gian xử lý, thêm X-Request-ID và X-Process-Time vào response, đồng thời log method, URL và status code.

OPTIONS request được chuyển tiếp bình thường và không yêu cầu JWT.

## 11. Cài đặt

Tạo môi trường ảo:

python -m venv .venv

Windows:

.venv\Scripts\activate

Linux/macOS:

source .venv/bin/activate

Cài thư viện:

pip install -r requirements.txt

Tạo .env:

copy .env.example .env

Tạo dữ liệu mẫu:

python seed.py

Chạy server:

uvicorn main:app --reload

Swagger:

http://127.0.0.1:8000/docs

Health:

http://127.0.0.1:8000/health

## 12. Tài khoản mẫu

Admin:

admin@example.com

Admin@123

User:

user@example.com

User@123

## 13. Frontend CORS

Mặc định cho phép:

http://localhost:3000

http://localhost:5173

Không sử dụng allow_origins=["*"] khi allow_credentials=True.

## 14. Cấu trúc

secure-learning-portal/
├── main.py
├── config.py
├── seed.py
├── requirements.txt
├── README.md
├── .env.example
├── database/
├── dependencies/
├── middleware/
├── models/
├── routers/
├── schemas/
├── security/
└── services/
