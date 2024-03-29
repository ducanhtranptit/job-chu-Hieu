Import dependencies:

-   `time`: Thư viện tiêu chuẩn Python để thực hiện các thao tác liên quan đến thời gian.
-   `OpenAI`: Module client để giao tiếp với API của OpenAI.
-   `dotenv`: Thư viện để load các biến môi trường từ một tệp .env.
-   `os`: Thư viện để truy cập các biến môi trường.
-   `pandas`: Thư viện Python cho các cấu trúc dữ liệu và công cụ phân tích dữ liệu.
-   `ast`: Thư viện cho phép phân tích cú pháp và xử lý biểu thức Python.
-   `scipy.spatial.distance.cosine`: Cung cấp các hàm để tính khoảng cách cosine giữa hai vectơ.

Khởi tạo các biến môi trường và tạo một client OpenAI:

-   Load các biến môi trường từ tệp .env sử dụng `dotenv`.
-   Lấy các giá trị cho `OPENAI_API_KEY`, `EMBEDDING_MODEL`, và `GPT_MODEL` từ biến môi trường.
-   Sử dụng các giá trị này để khởi tạo một đối tượng `OpenAI` cho việc giao tiếp với API của OpenAI.

Lớp `Assist`:

-   Định nghĩa một lớp để tương tác với hệ thống trợ lí ảo của OpenAI.
    -   `__init__(self, assist_id)`: Khởi tạo đối tượng `Assist` với một `assist_id` cho việc xác định người trợ lí ảo.
    -   `create_thread(self)`: Tạo một luồng mới trong hệ thống trợ lí ảo và trả về đối tượng luồng.
    -   `ask(self, thread_id, question)`: Đặt một câu hỏi cho hệ thống trợ lí ảo thông qua một luồng đã cho và trả về yêu cầu thực hiện và tin nhắn gửi câu hỏi.
    -   `wait_answer(self, run, thread_id)`: Đợi cho đến khi một yêu cầu thực hiện (run) hoàn thành và trả về kết quả.
    -   `answer(self, msg, thread_id)`: Trả về câu trả lời từ tin nhắn của hệ thống trợ lí ảo trong một luồng đã cho.
    -   `format_answer(self, m)`: Định dạng câu trả lời từ một tin nhắn.

Hàm `strings_ranked_by_relatedness`:

-   Sắp xếp các chuỗi dựa trên mức độ liên quan với một truy vấn.
-   Sử dụng một hàm liên quan đã được cung cấp hoặc mặc định là khoảng cách cosine để tính toán mức độ liên quan.
-   Trả về một danh sách các chuỗi và mức độ liên quan tương ứng.

Hàm `query_message`:

-   Tạo tin nhắn chứa các đoạn văn bản sắp xếp theo mức độ liên quan với một truy vấn.
-   Sử dụng các đoạn văn bản từ tệp CSV để tạo tin nhắn.
-   Cắt dữ liệu nếu vượt quá ngân sách về số lượng token.

Hàm `ask_using_embedding`:

-   Sử dụng mô hình nhúng để tạo câu trả lời cho một câu hỏi.
-   Sử dụng hàm `query_message` để tạo nội dung câu hỏi.
-   Gửi câu hỏi đến hệ thống và trả về câu trả lời.

Hàm `num_tokens`:

-   Đếm số lượng token trong một văn bản dựa trên một mô hình đã cho.

Với các hàm và lớp này, `openai_client.py` cung cấp các công cụ để tương tác với hệ thống trợ lí ảo của OpenAI và xử lý dữ liệu cho việc tạo câu hỏi và câu trả lời.
