import uuid
from django.db import models
from django.core.validators import RegexValidator

# --- Validators ---
CURRENCY_CODE_VALIDATOR = RegexValidator(
    regex=r"^[A-Z]{3}$",
    message="کد واحد پول باید سه حرف بزرگ انگلیسی (ISO-4217) باشد."
)

PHONE_VALIDATOR = RegexValidator(
    regex=r"^\+?[0-9\-\s]{7,20}$",
    message="شماره تلفن نامعتبر است."
)

TIMEZONE_MAX_LENGTH = 64  # طول منطقی برای نام‌های IANA timezone


class Organization(models.Model):
    """
    Core business entity. Holds legal/commercial identity and default accounting context.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="شناسه یکتا",
    )

    # Identity
    legal_name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="نام/عنوان حقوقی سازمان/شرکت/فروشگاه",
    )
    trade_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="نام تجاری (برند)",
    )
    registration_code = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="شناسه ملی / کد اقتصادی",
    )

    # Contact / Address
    country = models.CharField(
        max_length=100,
        default="Iran",
        verbose_name="کشور",
    )
    state_province = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="استان/ایالت",
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="شهر",
    )
    address_line1 = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="آدرس - سطر ۱",
    )
    address_line2 = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="آدرس - سطر ۲",
    )
    postal_code = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="کدپستی",
    )
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        validators=[PHONE_VALIDATOR],
        verbose_name="تلفن تماس",
    )
    email_address = models.EmailField(
        blank=True,
        verbose_name="ایمیل",
    )

    # Defaults / Context
    timezone = models.CharField(
        max_length=TIMEZONE_MAX_LENGTH,
        default="Asia/Tehran",
        verbose_name="منطقه زمانی (IANA)",
    )
    currency_code = models.CharField(
        max_length=3,
        default="IRR",
        validators=[CURRENCY_CODE_VALIDATOR],
        verbose_name="کد واحد پول (ISO-4217)",
    )
    extra_settings = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="تنظیمات اضافه",
    )

    # Status & Timestamps
    is_active = models.BooleanField(
        default=True,
        verbose_name="فعال؟",
    )
    is_delete = models.BooleanField(
        default=False,
        verbose_name="حذف شده؟",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="تاریخ بروزرسانی",
    )

    class Meta:
        db_table = "organizations"
        verbose_name = "سازمان"
        verbose_name_plural = "سازمان‌ها"
        ordering = ["legal_name"]
        indexes = [
            models.Index(fields=["legal_name"], name="org_legal_name_idx"),
            models.Index(fields=["is_active"], name="org_active_idx"),
        ]

    def __str__(self) -> str:
        return self.legal_name
