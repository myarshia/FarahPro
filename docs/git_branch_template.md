# FarahPro - Git Branch Template

## شاخه‌های اصلی

| Branch Name | توضیح | وضعیت |
|-------------|-------|-------|
| `main` | نسخه پایدار، همیشه قابل انتشار | 🟢 Stable |
| `develop` | نسخه توسعه اصلی، ادغام فیچرها | 🔵 In Progress |

---

## شاخه‌های فیچر (Feature Branches)

📌 همه فیچرها باید از روی `develop` ساخته شوند.

| Branch Name | توضیح |
|-------------|-------|
| `feature/core-common` | کدهای پایه، middleware، ابزارهای مشترک |
| `feature/accounts` | سیستم کاربران، نقش‌ها، مجوزها |
| `feature/organizations` | مدیریت شرکت/کسب‌وکار (Multi-Tenant) |
| `feature/stores` | مدیریت فروشگاه‌ها (در صورت نیاز جدا) |
| `feature/chart-of-accounts` | سرفصل‌ها، حساب‌ها، ترازها |
| `feature/transactions` | تراکنش‌ها، ثبت و ویرایش |
| `feature/invoices` | فاکتورها، رسیدها، پرداخت‌ها |
| `feature/reporting` | گزارش‌های مالی، ترازنامه |
| `feature/imports-exports` | ایمپورت/اکسپورت CSV و اکسل |
| `feature/api` | REST/GraphQL API و نسخه‌بندی |
| `feature/web-frontend` | صفحات و رابط کاربری وب |
| `feature/integrations` | درگاه پرداخت، پیامک، ایمیل |
| `feature/tasks` | پردازش‌های پس‌زمینه و زمان‌بندی |
| `feature/admin-panel` | پنل مدیریت سیستم |
| `feature/tests` | تست‌های خودکار و Fixtures |
| `feature/auditlog` | ثبت لاگ تغییرات و حسابرسی |

---

## قوانین کلی
1. **هر شاخه فیچر** از `develop` ساخته شود.
2. **Commit**‌ها باید واضح و توصیفی باشند.
3. بعد از اتمام فیچر → Merge به `develop`.
4. قبل از انتشار نسخه پایدار → Merge `develop` به `main`.
5. روی `main` مستقیم کد نزن مگر برای Hotfix فوری.

---

## رنگ‌بندی پیشنهادی در PyCharm
- `main` → سبز تیره 🟢  
- `develop` → آبی 🔵  
- فیچرها → رنگ‌های روشن متنوع 🌈

---

📅 تهیه‌کننده: Meghdad Mahboobi
🛠 برای پروژه **FarahPro**
