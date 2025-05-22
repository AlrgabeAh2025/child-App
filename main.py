# استيراد المكتبات الضرورية
from flet import *
from views.login_screen.login_screen import Login
from views.signup_screen.signup_screen import SignUp
from views.welcome_screen.welcome_screen import Welcome
import requests
from views.home_screen.home_screen import Home
from views.profile_screen.profile_screen import (
    Profile,
    PersonalInformation,
    SecurityPasswords,
)

# تعريف الدالة الرئيسية للتطبيق
def main(page: Page):

    # تعريف الخطوط المستخدمة في التطبيق
    page.fonts = {
        "LateefBoldFont": "/fonts/Lateef,Rakkas/Lateef/Lateef-Bold.ttf",
        "LateefNormalFont": "/fonts/Lateef,Rakkas/Lateef/Lateef-Medium.ttf",
        "Rakkas": "/fonts/Lateef,Rakkas/Rakkas/Rakkas-Regular.ttf",
        "ElMessiri": "/fonts/El_Messiri,Lateef,Rakkas/El_Messiri/ElMessiri-VariableFont_wght.ttf",
    }

    # تعيين وضع الثيم والنص من اليمين إلى اليسار
    page.theme_mode = ThemeMode.LIGHT
    page.rtl = True

    # تعريف الثيم الخاص بالتطبيق
    page.theme = Theme(
        font_family="LateefNormalFont",  # نوع الخط الافتراضي
        color_scheme_seed="#666666",  # لون البذرة للثيم
        text_theme=TextStyle(color="#110b22", font_family="LateefBoldFont"),  # تخصيص نمط النص
        appbar_theme=AppBarTheme(bgcolor="#110b22", color="#ffffff"),  # تخصيص شريط التطبيق
    )

    baseUrl = "https://himya.justhost.ly"  # الرابط الأساسي للخادم
    # page.client_storage.clear()  # مسح التخزين المحلي (معلق حالياً)

    # دالة لعرض رسائل للمستخدم
    def showMessage(text):
        snack_bar = SnackBar(
            content=Text(
                f"{text}",
                style=TextStyle(size=15, font_family="ElMessiri"),  # تخصيص نمط النص
            ),
            show_close_icon=True  # إظهار أيقونة الإغلاق
        )
        page.open(snack_bar)  # عرض الرسالة

    # دالة لتغيير المسارات (Routes) بين الشاشات
    def route_change(e):
        routes = {
            "/": Welcome,  # شاشة الترحيب
            "/home": Home,  # الشاشة الرئيسية
            "/login": Login,  # شاشة تسجيل الدخول
            "/signup": SignUp,  # شاشة إنشاء الحساب
            "/Profile": Profile,  # شاشة الملف الشخصي
            "/PersonalInformation": PersonalInformation,  # شاشة تعديل المعلومات الشخصية
            "/SecurityPasswords": SecurityPasswords,  # شاشة تغيير كلمة المرور
        }

        # استدعاء دالة will_unmount إذا كانت موجودة في الشاشة الحالية
        for view in page.views:
            if hasattr(view, "will_unmount"):  # إذا كانت الدالة موجودة
                view.will_unmount()

        # جلب الشاشة المناسبة بناءً على المسار
        page_class = routes.get(page.route, None)
        page_class.baseUrl = baseUrl  # تعيين الرابط الأساسي للشاشة
        if page_class:
            page.views.append(
                page_class(route=page.route, page=page)  # إضافة الشاشة المناسبة
            )
        else:
            page.views.append(Text("Page not found"))  # إذا لم يكن المسار موجودًا
        page.update()  # تحديث الصفحة

    # دالة لتحديث token الوصول
    def refreshAccessToken():
        if not page.client_storage.contains_key("refresh"):  # إذا لم يكن هناك توكن تحديث
            return [False, "سجل الدخول أو أنشئ حساب"]  # إرجاع رسالة خطأ

        # دالة غير متزامنة لتحديث token الوصول
        async def refresh(refresh_token):
            body = {"refresh": refresh_token}  # إعداد بيانات الطلب
            try:
                response = requests.post(url=f"{baseUrl}/refresh/", data=body)  # إرسال الطلب
                if response.status_code == 200:  # إذا كان الطلب ناجحًا
                    json_data = response.json()  # تحويل الاستجابة إلى JSON
                    return [True, json_data]  # إرجاع النتيجة الناجحة
                else:
                    return [False, "الرجاء التحقق من اتصال الانترنت"]  # إرجاع رسالة خطأ
            except requests.exceptions.Timeout:  # التعامل مع انقطاع الاتصال
                return [False, "الرجاء التحقق من اتصال الانترنت"]
            except requests.exceptions.ConnectionError:  # التعامل مع أخطاء الاتصال
                return [False, "لم نتمكن من الوصول إلى الخادم، الرجاء إعادة المحاولة"]

        refresh_token = page.client_storage.get("refresh")  # الحصول على توكن التحديث
        result = page.run_task(refresh, refresh_token).result()  # إرسال الطلب بشكل غير متزامن

        if result[0]:  # إذا كان التحديث ناجحًا
            page.client_storage.set("access", result[1]['access'])  # حفظ توكن الوصول الجديد
            page.client_storage.set("refresh", result[1]['refresh'])  # حفظ توكن التحديث الجديد
        return result  # إرجاع النتيجة

    # تعيين دالة تغيير المسار كمعالج حدث
    page.on_route_change = route_change

    # محاولة تحديث token الوصول
    result = refreshAccessToken()
    if result[0]:  # إذا كان التحديث ناجحًا
        page.go("/home")  # الانتقال إلى الشاشة الرئيسية
    else:
        page.go("/")  # الانتقال إلى شاشة الترحيب
        showMessage(result[1])  # عرض رسالة الخطأ

# تشغيل التطبيق
app(main, assets_dir="assets")
