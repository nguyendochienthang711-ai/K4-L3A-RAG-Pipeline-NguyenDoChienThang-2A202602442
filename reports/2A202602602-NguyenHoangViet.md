# Báo cáo đóng góp cá nhân

## Thông tin

- Họ và tên: Nguyễn Hoàng Việt
- Mã học viên: 2A202602602
- Nhóm: BungChay
- Vai trò: Generation / UI
- Repository/branch: `K4-L3A-RAG-Pipeline-NguyenDoChienThang-2A202602442` / `viet` (PR #4 đã gộp vào `main`)

## Phần việc đã thực hiện

| Module/deliverable | Việc tôi trực tiếp làm | File/commit/PR | Trạng thái |
|---|---|---|---|

| Streamlit Application & UI (App) | Xây dựng ứng dụng Streamlit hoàn chỉnh cho UniLib Bot gồm 2 chế độ: Landing Screen (chips câu hỏi nhanh, grid quy định cốt lõi) và Active Chat Screen (message bubbles, trích dẫn citation, expandable sources, disclaimer). | [app.py](../app.py), [.streamlit/config.toml](../.streamlit/config.toml), [assets/owl_bot.jpg](../assets/owl_bot.jpg); commit `02a927c`, `2f8333b`, PR #4 | Done |
| Sidebar & Design System | Thiết kế sidebar chuẩn thương hiệu: Header UniLib Bot, nút "Đoạn chat mới" (phím tắt Ctrl+K), phân nhóm lịch sử chat ("HÔM NAY", "7 NGÀY QUA"), và User Profile Footer ghim sát đáy; tối ưu CSS layout loại bỏ khoảng trống thừa trên đỉnh (padding-top). | [app.py](../app.py) | Done |
| Tích hợp luồng RAG vào UI | Kết nối hàm `generate_with_citation` vào giao diện Streamlit, hiển thị câu trả lời với trích dẫn rõ ràng, hiển thị danh sách context chunks, score tương đồng và phương thức retrieval (`hybrid`/`pageindex`). | [app.py](../app.py) | Done |

*Chỉ kê khai công việc có thể đối chiếu bằng file, commit, pull request, test hoặc kết quả evaluation. Tôi không nhận phần data crawling hay retrieval/indexing của các role khác.*

## Quyết định kỹ thuật quan trọng

1. **Quyết định: Áp dụng kỹ thuật Reordering (`reorder_for_llm`) cho các context chunks trước khi đưa vào prompt của LLM.**  
   **Lý do/evidence:** Hiện tượng "Lost-in-the-middle" khiến LLM thường chú ý nhiều nhất vào phần đầu và phần cuối của context dài, dễ bỏ qua các chunks nằm ở giữa. Bằng cách đan xen đưa các chunks có điểm liên quan cao nhất về hai đầu (`chunks[::2]` và `chunks[1::2][::-1]`), mô hình nắm bắt thông tin quan trọng tốt hơn, tăng độ chính xác của trích dẫn citation `[Document X]`.  
   **Trade-off:** Xáo trộn thứ tự tuyến tính ban đầu của kết quả retrieval, nhưng metadata vẫn giữ nguyên đánh số thứ tự tài liệu rõ ràng nên không ảnh hưởng đến tính minh bạch của nguồn.

2. **Quyết định: Thiết kế luồng UI hai trạng thái (Landing Screen với gợi ý nhanh và Active Chat Screen) kết hợp cơ chế Safe Refusal trực quan.**  
   **Lý do/evidence:** Người dùng thư viện (đặc biệt tân sinh viên) thường chưa biết bắt đầu hỏi từ đâu; Landing Screen với các thẻ quy định cốt lõi và quick action chips giúp định hướng nhu cầu ngay lập tức. Khi câu hỏi nằm ngoài phạm vi tài liệu đã thu thập, hệ thống trả về câu từ chối an toàn chuẩn ("Tôi không thể xác minh thông tin này từ nguồn hiện có.") thay vì để mô hình bịa đặt thông tin gây hiểu lầm quy chế nhà trường.  
   **Trade-off:** Cần quản lý `session_state` và CSS tùy biến phức tạp hơn so với giao diện chat Streamlit mặc định, đồng thời câu trả lời bị ràng buộc chặt chẽ vào context được cung cấp.

## Kiểm thử và kết quả

- Test hoặc query tôi đã dùng: `pytest tests/test_contracts.py -k "test_task10_generation_contract"` và chạy thử nghiệm thực tế trên UI Streamlit với các câu hỏi in-domain ("Thời gian mượn sách giáo trình", "Mức phí phạt trễ hạn", "Gia hạn sách online") và out-of-domain ("Thủ tục đăng ký thi lại đại học").
- Kết quả trước/sau nếu có: Module Task 10 đạt 100% test contract; giao diện Streamlit phản hồi mượt mà, hiển thị đầy đủ nhãn trích dẫn `[Document X]`, đúng nguồn và điểm retrieval score. Câu hỏi out-of-domain trả về đúng thông báo Safe Refusal.
- Lỗi đã phát hiện và cách xử lý:
  - Selector CSS của sidebar footer ban đầu (`> div:has(...)`) vô tình áp dụng `margin-top: auto` lên toàn bộ container cha của Streamlit khiến nội dung sidebar bị dồn xuống đáy và tạo khoảng trắng lớn ở trên đỉnh (`padding-top`). Đã khắc phục bằng cách thu hẹp bộ chọn chính xác vào container của footer (`.stElementContainer:has(.sidebar-user-footer)`), đồng thời chuyển `justify-content` thành `flex-start`.
  - Xử lý các trường hợp query rỗng hoặc lỗi provider không có API key bằng cách trả về `SAFE_REFUSAL` có cấu trúc thay vì throw exception làm crash ứng dụng.

## Điều còn hạn chế

- Một hạn chế cụ thể của phần tôi làm: Hiện tại UI Streamlit hiển thị câu trả lời dạng block hoàn chỉnh một lần thay vì streaming từng token (`st.write_stream`), do cần trích xuất và highlight citation đồng thời từ cấu trúc dữ liệu trả về của Task 10.
- Nếu có thêm thời gian, thay đổi đầu tiên tôi sẽ thực hiện: Triển khai streaming response kết hợp parser tự động phát hiện và render các thẻ citation `[Document X]` dạng hover tooltip/popover ngay trong lúc stream.

## Xác nhận đóng góp

Tôi xác nhận nội dung trên phản ánh đúng phần việc của mình và có thể giải thích hoặc chạy lại trong buổi demo.

- Ngày: 20/09/2026
- Tên thành viên: Nguyễn Hoàng Việt
