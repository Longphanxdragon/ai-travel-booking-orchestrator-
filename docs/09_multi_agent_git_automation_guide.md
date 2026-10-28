# 🤖 CẨM NANG MULTI-AGENT DEVELOPMENT & GIT AUTOMATION (CI/CD)

---

## 1. CÔNG VIỆC ĐIỀU KHIỂN GIT, MERGE & KIỂM THỬ GỌI LÀ GÌ?

Trong ngành kỹ thuật phần mềm hiện đại, công việc này được gọi là:
1. **CI/CD Automation (Continuous Integration / Continuous Deployment)**: Tích hợp và Triển khai Liên tục.
2. **Release Engineering / DevOps**: Kỹ sư phụ trách chất lượng bản phát hành, tự động hóa kiểm thử và đóng gói phần mềm.
3. Khi áp dụng AI vào quản lý quy trình này, thuật ngữ mới nhất năm 2026 gọi là **AI DevOps Agent** hoặc **AI Code Reviewer & Gatekeeper Agent**.

---

## 2. CÓ CON AGENT NÀO TỰ ĐỘNG KIỂM THỬ, TẠO BRANCH & MERGE CODE KHÔNG?

**CÓ, VÀ ĐÂY LÀ NHỮNG CON AGENT / CÔNG CỤ CHUẨN CÔNG NGHIỆP TỐT NHẤT HIỆN NAY:**

### A. Tự động hóa qua GitHub Actions (Native & Miễn phí 100%) - *TÔI VỪA CÀI CHO BẠN!*
- Tôi vừa tạo file [`.github/workflows/ci.yml`](.github/workflows/ci.yml) và đẩy lên GitHub của bạn.
- **Cơ chế hoạt động:** Mỗi khi bạn, Cursor hoặc Claude đẩy code lên hoặc tạo Pull Request (PR), một con "Robot Runner" trên GitHub sẽ tự động:
  1. Kéo code về môi trường Ubuntu ảo.
  2. Chạy toàn bộ bài test kiểm tra tính hợp lệ của Pydantic Schemas và pipeline bảo mật PII.
  3. Nếu test **FAIL (bị lỗi)** ➔ Nó khóa nút Merge lại, không cho gộp code hỏng vào nhánh `main`.
  4. Nếu test **PASS (thành công)** ➔ Hiện tích xanh ✅ cho phép merge an toàn!

### B. Các AI Reviewer & Automation Agents nổi tiếng:
1. **Coderabbit.ai (AI Code Review Agent)**: 
   - Cài trực tiếp từ GitHub Marketplace vào repo của bạn (miễn phí cho repo cá nhân/open-source).
   - Mỗi khi bạn mở một Pull Request, CodeRabbit sẽ đọc toàn bộ code diff, chỉ ra lỗi tiềm ẩn, gợi ý sửa code và tự viết tóm tắt thay đổi.
2. **Sweep.dev / Devin**:
   - Tác tử AI chuyên nhận Issue từ GitHub, tự tạo Branch mới, tự viết code, tự chạy test và mở Pull Request để bạn duyệt.

---

## 3. CÁCH DÙNG CURSOR HOẶC CLAUDE LÀM VIỆC SONG SONG MÀ KHÔNG BỊ XUNG ĐỘT (CONFLICT)

Bạn hoàn toàn có thể dùng **Cursor**, **Claude Code** hoặc tôi làm việc cùng lúc trên cùng một dự án theo **Chiến lược Phân nhánh Git chuẩn (Git Flow)**:

```text
               (Nhánh chính: Luôn sạch sẽ, đã test kỹ)
main ───────────●────────────────────────────────────────● (v1.0 Release)
                 \                                      /
                  \ (Tạo Pull Request - CI Test Pass)  /
feature/latex      ●──────────────●───────────────────● (Bạn hoặc Tôi viết Báo cáo)
                    \                                /
feature/backend      ●─────────────●────────────────● (Cursor / Claude code tính năng)
```

### Quy trình 3 bước phối hợp song song:
1. **Quy tắc 1 nhánh 1 việc (Branch per Feature):**
   - Khi bảo **Cursor** code backend: Bảo Cursor gõ `git checkout -b feature/core-agent`.
   - Khi bảo **Tôi** viết Báo cáo LaTeX: Viết trên nhánh `feature/thesis-latex`.
2. **Kéo code mới nhất trước khi làm việc:**
   - Trước khi bắt đầu ca làm việc trên Cursor hoặc Claude, luôn gõ:
     ```bash
     git pull origin main
     ```
3. **Mở Pull Request (PR) để GitHub Runner kiểm tra:**
   - Sau khi code xong trên nhánh phụ, đẩy lên GitHub và bấm nút **"Create Pull Request"**.
   - Robot CI mà tôi vừa cài sẽ tự động chạy test. Thấy tích xanh ✅ thì bạn chỉ việc bấm nút **Merge** là xong!
