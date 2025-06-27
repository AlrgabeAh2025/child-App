import qrcode, base64, requests
from io import BytesIO
from flet import *
import asyncio


class Home(View):

    # دالة البناء (Constructor)
    # تهيئة الكلاس وتعيين المتغيرات الأولية
    def __init__(self, route, page):
        super().__init__(route=route)  # استدعاء مُنشئ الفئة الأم (View)
        self.page = page  # تعيين الصفحة الحالية
        self.scroll = ScrollMode.ALWAYS  # تمكين التمرير دائمًا
        self.screenShotState = False  # حالة مراقبة الشاشة (إيقاف بشكل افتراضي)
        self.UsageStatsState = (
            False  # حالة مراقبة استخدام التطبيقات (إيقاف بشكل افتراضي)
        )
        self.checkIsThereFatherVar = True  # متغير للتحقق من وجود أب مرتبط

        # إنشاء قائمة التنقل الجانبية
        self.drawer = NavigationDrawer(
            on_change=self.handle_change,  # حدث تغيير العنصر المحدد
            controls=[
                Container(height=12),  # مسافة بين العناصر
                NavigationDrawerDestination(
                    label="الرئيسية",  # عنصر القائمة الرئيسية
                    icon_content=Icon(icons.HOME_OUTLINED),  # أيقونة غير محددة
                    selected_icon_content=Icon(icons.HOME),  # أيقونة محددة
                ),
                NavigationDrawerDestination(
                    label="تسجيل الخروج",  # عنصر تسجيل الخروج
                    icon_content=Icon(icons.LOGOUT_OUTLINED),  # أيقونة غير محددة
                    selected_icon_content=Icon(icons.LOGOUT),  # أيقونة محددة
                ),
            ],
        )

        # إنشاء شريط التطبيق (AppBar)
        self.appbar = AppBar(
            actions=[
                IconButton(
                    icon=icons.PERSON,  # أيقونة الملف الشخصي
                    icon_color="#ffffff",  # لون الأيقونة
                    on_click=lambda x: self.page.go(
                        "/Profile"
                    ),  # حدث النقر للانتقال إلى الملف الشخصي
                ),
            ],
            leading=IconButton(
                icon=icons.MENU,  # أيقونة القائمة
                icon_color="#ffffff",  # لون الأيقونة
                on_click=lambda e: self.page.open(
                    self.drawer
                ),  # حدث النقر لفتح القائمة الجانبية
            ),
            toolbar_height=100,  # ارتفاع شريط التطبيق
            title=Text(
                "حماية الاطفال",  # عنوان شريط التطبيق
                size=20,
                weight=FontWeight.BOLD,
                color="#ffffff",  # لون النص
                font_family="ElMessiri",  # نوع الخط
            ),
        )

    # دالة نسخ النص إلى الحافظة
    # تقوم بنسخ النص الممرر إليها وعرض رسالة تأكيد
    def copy(self, data):
        self.page.set_clipboard(data)  # نسخ النص إلى الحافظة
        self.page.open(
            SnackBar(Text("تم نسخ المفتاح"), open=True)
        )  # عرض رسالة نجاح النسخ
        self.page.update()  # تحديث الصفحة

    # دالة عرض واجهة المستخدم عندما لا يوجد أب مرتبط
    # تعرض واجهة تحتوي على رمز QR ومفتاح المستخدم للاقتران
    def hasNoFather(self, userData):
        self.scroll = ScrollMode.ALWAYS  # تمكين التمرير
        qr = self.generateQr(userData)  # إنشاء رمز QR
        self.controls.clear()  # مسح العناصر الحالية
        self.controls.append(
            ResponsiveRow(
                controls=[
                    Container(
                        content=Column(
                            controls=[
                                ListTile(
                                    leading=Icon(icons.INFO),  # أيقونة المعلومات
                                    title=Text(
                                        "امسح رمز (QR) بالاسفل للاقتران بهاذة الجهاز",  # نص التعليمات
                                        size=13,
                                        weight=FontWeight.NORMAL,
                                        color="#666666",  # لون النص
                                        font_family="ElMessiri",  # نوع الخط
                                    ),
                                ),
                                Container(
                                    content=Text(
                                        "اولا يجب ان تقوم بإنشاء حساب في هاتف الاب ثم يمكنك مسح رمز (QR) بالاسفل للاقتران مع هذا الجهاز",  # نص التعليمات
                                        size=13,
                                        weight=FontWeight.NORMAL,
                                        color="#666666",  # لون النص
                                        font_family="ElMessiri",  # نوع الخط
                                    ),
                                    padding=10,  # الحشو الداخلي
                                ),
                            ]
                        ),
                        bgcolor="#ffffff",  # لون الخلفية
                        border=border.all(color="#110b22", width=1),  # إطار الحاوية
                        border_radius=border_radius.all(10),  # حواف مستديرة
                    ),
                    Container(height=10),  # مسافة بين العناصر
                    Container(
                        content=Text(
                            "ادخل هذا في هاتف الاب للأقتران بالجهاز",  # نص التعليمات
                            size=13,
                            weight=FontWeight.NORMAL,
                            color="#666666",  # لون النص
                            font_family="ElMessiri",  # نوع الخط
                        ),
                    ),
                    Container(
                        content=ListTile(
                            title=Text(
                                f"{userData['key']}",  # عرض مفتاح المستخدم
                                style=TextStyle(
                                    size=11,
                                    weight=FontWeight.BOLD,
                                    font_family="ElMessiri",  # نوع الخط
                                ),
                            ),
                            trailing=IconButton(
                                icon=icons.COPY,  # أيقونة النسخ
                            ),
                        ),
                        bgcolor="#ffffff",  # لون الخلفية
                        border=border.all(0.5, "#110b22"),  # إطار الحاوية
                        border_radius=border_radius.all(5),  # حواف مستديرة
                        on_click=lambda x: self.copy(f"{userData['key']}"),  # حدث النسخ
                    ),
                    Container(height=10),  # مسافة بين العناصر
                    Container(
                        content=Text(
                            "أو إمسح رمز (QR) للحصول على المفتاح",  # نص التعليمات
                            size=13,
                            weight=FontWeight.NORMAL,
                            color="#666666",  # لون النص
                            font_family="ElMessiri",  # نوع الخط
                        ),
                    ),
                    Container(
                        content=Column(
                            controls=[
                                Image(src_base64=qr, width=200),  # عرض رمز QR
                                Container(
                                    content=Text(
                                        "امسح رمز (QR)",  # نص التعليمات
                                        size=14,
                                        weight=FontWeight.NORMAL,
                                        color="#666666",  # لون النص
                                        font_family="ElMessiri",  # نوع الخط
                                    ),
                                ),
                            ],
                            horizontal_alignment=CrossAxisAlignment.CENTER,  # محاذاة العناصر في المنتصف
                            alignment=MainAxisAlignment.CENTER,  # محاذاة العناصر في المنتصف
                        ),
                        bgcolor="#ffffff",  # لون الخلفية
                        border=border.all(color="#110b22", width=1),  # إطار الحاوية
                        border_radius=border_radius.all(10),  # حواف مستديرة
                        padding=padding.symmetric(vertical=10),  # الحشو الداخلي
                    ),
                ],
                expand=True,  # توسيع الصف لملء المساحة المتاحة
            )
        )
        self.update()  # تحديث الواجهة

    # دالة عرض واجهة المستخدم عندما يوجد أب مرتبط
    # تعرض واجهة تحتوي على معلومات الأب وخيارات المراقبة
    def hasFatherScreen(self, userData):
        self.controls.clear()  # مسح العناصر الحالية
        self.scroll = ScrollMode.ALWAYS  # تمكين التمرير
        self.controls.append(
            ResponsiveRow(
                controls=[
                    Container(height=10),  # مسافة بين العناصر
                    Column(
                        controls=[
                            Container(
                                content=Image(
                                    src=(
                                        "images/father.png"
                                        if f"{userData['father_gender']}" == "1"
                                        else "images/mather.png"
                                    ),  # عرض صورة الأب أو الأم بناءً على الجنس
                                    width=150,  # عرض الصورة
                                ),
                            ),
                            Container(
                                content=Text(
                                    f"{userData['father_first_name']}",  # عرض اسم الأب الأخير
                                    size=20,
                                    weight=FontWeight.BOLD,
                                    color="#666666",  # لون النص
                                    font_family="ElMessiri",  # نوع الخط
                                ),
                            ),
                            Container(height=20),  # مسافة بين العناصر
                            ResponsiveRow(
                                controls=[
                                    Text(
                                        "البيانات التي يتم مراقبتها",  # نص العنوان
                                        style=TextStyle(
                                            size=12,
                                            weight=FontWeight.BOLD,
                                            font_family="ElMessiri",  # نوع الخط
                                        ),
                                        color="#666666",  # لون النص
                                        text_align=TextAlign.START,  # محاذاة النص
                                    ),
                                ],
                            ),
                            Container(
                                content=ResponsiveRow(
                                    controls=[
                                        ListTile(
                                            title=Text(
                                                "مراقبة استخدام التطبيقات",  # نص العنصر
                                                style=TextStyle(
                                                    size=14,
                                                    weight=FontWeight.BOLD,
                                                    font_family="ElMessiri",  # نوع الخط
                                                ),
                                            ),
                                            trailing=Switch(
                                                value=self.UsageStatsState,  # حالة التبديل
                                                active_color="#110b22",  # لون التبديل عند التفعيل
                                                on_change=self.startGetUsageStats,  # حدث التغيير
                                            ),
                                            subtitle=Text(
                                                "مغلق",  # نص الحالة
                                                style=TextStyle(
                                                    size=10,
                                                    weight=FontWeight.BOLD,
                                                    font_family="ElMessiri",  # نوع الخط
                                                ),
                                            ),
                                        ),
                                    ],
                                ),
                                bgcolor="#ffffff",  # لون الخلفية
                                border=border.all(0.5, "#110b22"),  # إطار الحاوية
                                border_radius=border_radius.all(5),  # حواف مستديرة
                                alignment=alignment.center,  # محاذاة العناصر في المنتصف
                            ),
                            Container(
                                content=ResponsiveRow(
                                    controls=[
                                        ListTile(
                                            title=Text(
                                                "مراقبة الشاشة",  # نص العنصر
                                                style=TextStyle(
                                                    size=14,
                                                    weight=FontWeight.BOLD,
                                                    font_family="ElMessiri",  # نوع الخط
                                                ),
                                            ),
                                            trailing=Switch(
                                                value=self.screenShotState,  # حالة التبديل
                                                active_color="#110b22",  # لون التبديل عند التفعيل
                                                on_change=self.startGetScreenShot,  # حدث التغيير
                                            ),
                                            subtitle=Text(
                                                "مغلق",  # نص الحالة
                                                style=TextStyle(
                                                    size=10,
                                                    weight=FontWeight.BOLD,
                                                    font_family="ElMessiri",  # نوع الخط
                                                ),
                                            ),
                                        ),
                                    ],
                                ),
                                bgcolor="#ffffff",  # لون الخلفية
                                border=border.all(0.5, "#110b22"),  # إطار الحاوية
                                border_radius=border_radius.all(5),  # حواف مستديرة
                                alignment=alignment.center,  # محاذاة العناصر في المنتصف
                            ),
                            Container(height=20),  # مسافة بين العناصر
                        ],
                        horizontal_alignment=CrossAxisAlignment.CENTER,  # محاذاة العناصر في المنتصف
                        alignment=MainAxisAlignment.CENTER,  # محاذاة العناصر في المنتصف
                    ),
                ],
                expand=True,  # توسيع الصف لملء المساحة المتاحة
            )
        )
        self.update()  # تحديث الواجهة

    # دالة يتم تنفيذها عند تحميل الصفحة
    # تهيئة الحالات الأولية وبدء المهام اللازمة
    def did_mount(self):
        self.screenShotState = self.page.client_storage.get(
            "screenShotState"
        )  # الحصول على حالة مراقبة الشاشة
        self.UsageStatsState = self.page.client_storage.get(
            "UsageStatsState"
        )  # الحصول على حالة مراقبة التطبيقات
        self.page.run_task(self.getUsageStats)  # بدء مراقبة استخدام التطبيقات
        self.page.run_task(self.getBackground)  # بدء مراقبة الشاشة
        self.loaderUi()  # عرض واجهة التحميل
        self.checkIsThereFather()  # التحقق من وجود أب مرتبط
        self.page.run_task(self.checkIsTherFatherLoop)  # بدء مهمة التحقق المستمر من وجود أب

    # دالة إنشاء رمز QR باستخدام مفتاح المستخدم
    # تقوم بإنشاء رمز QR وتعيده كسلسلة نصية مشفرة بـ base64
    def generateQr(self, userData):
        qrCode = qrcode.make(f"{userData['key']}")  # إنشاء رمز QR
        buffered = BytesIO()  # إنشاء مخزن مؤقت للصورة
        qrCode.save(buffered, format="PNG")  # حفظ رمز QR كصورة PNG
        sl = base64.b64encode(buffered.getvalue())  # تشفير الصورة بـ base64
        resultOfQr = sl.decode("utf-8")  # تحويل النتيجة إلى سلسلة نصية
        return resultOfQr  # إرجاع رمز QR

    # دالة إرسال طلب HEAD إلى الخادم
    # تقوم بإرسال طلب HEAD للتحقق من وجود أب مرتبط
    async def sendHeadRequest(self, url, body={}):
        access = await self.page.client_storage.get_async(
            "access"
        )  # الحصول على رمز الوصول
        headers = {
            "Authorization": f"Bearer {access}",
            "Accept": "*/*",
            "Cache-Control": "no-cache",
        }
        try:
            response = requests.get(
                url=f"{Home.baseUrl}/{url}/?type=", data=body, headers=headers, timeout=30
            )
            json = response.json()  # تحويل الاستجابة إلى JSON
            if response.status_code == 200:
                userData = (
                    {
                        "username": json["username"],
                        "gender": json["gender"],
                        "first_name": json["first_name"],
                        "last_name": json["last_name"],
                        "profileImage": json["profileImage"],
                        "key": json["key"],
                    }
                    if not json.get("father_gender", None)
                    else {
                        "username": json["username"],
                        "gender": json["gender"],
                        "first_name": json["first_name"],
                        "last_name": json["last_name"],
                        "profileImage": json["profileImage"],
                        "key": json["key"],
                        "father_last_name": json["father_last_name"],
                        "father_gender": json["father_gender"],
                        "father_first_name": json["father_first_name"],
                    }
                )
                if json.get("father_gender", None):
                    await self.page.client_storage.set_async("userData", userData)
                    return [True, "has"]  # إرجاع النتيجة إذا كان هناك أب
                else:
                    await self.page.client_storage.set_async("userData", userData)
                    return [False, "hasNo"]  # إرجاع النتيجة إذا لم يكن هناك أب
        except requests.exceptions.Timeout:
            return [False, "اتصال الانترنت بطئ"]  # إرجاع رسالة خطأ في حالة انتهاء المهلة
        except requests.exceptions.ConnectionError:
            return [False, "حدث خطأ في الاتصال بالخادم. تحقق من اتصالك بالإنترنت."]  # إرجاع رسالة خطأ في حالة فشل الاتصال

    # دالة مراقبة الشاشة ورفع لقطات الشاشة إلى الخادم
    # تقوم بالتقاط لقطات الشاشة ورفعها إلى الخادم بشكل دوري
    async def getBackground(self):
        access = await self.page.client_storage.get_async(
            "access"
        )  # الحصول على رمز الوصول
        headers = {
            "Authorization": f"Bearer {access}",
            "Accept": "*/*",
            "Cache-Control": "no-cache",
        }
        while self.screenShotState:
            try:
                requests.get("https://www.google.com", timeout=5)
            except requests.exceptions.ConnectionError:
                await asyncio.sleep(5)
                continue

            try:
                response = requests.post("http://localhost:8080/screenshot")
                if response.status_code == 200:
                    files = {"file": ("screenshot.png", response.content, "image/png")}
                    upload_response = requests.put(
                        f"{Home.baseUrl}/Analysis/", files=files, headers=headers
                    )

                    if upload_response.status_code == 200:
                        print("✅ تم رفع الصورة بنجاح")
                    else:
                        print(f"⚠️ خطأ أثناء رفع الصورة: {upload_response.text}")
                else:
                    print("❌ لم يتم التقاط لقطة الشاشة بنجاح")

            except requests.exceptions.RequestException as e:
                print(f"⚠️ خطأ في الطلب: {e}")

            if not self.screenShotState:
                break

            await asyncio.sleep(5)

    # دالة مراقبة استخدام التطبيقات ورفع البيانات إلى الخادم
    # تقوم بجمع بيانات استخدام التطبيقات ورفعها إلى الخادم بشكل دوري
    async def getUsageStats(self):
        access = await self.page.client_storage.get_async(
            "access"
        )  # الحصول على رمز الوصول
        headers = {
            "Authorization": f"Bearer {access}",
            "Accept": "*/*",
            "Cache-Control": "no-cache",
        }
        while self.UsageStatsState:
            try:
                requests.get("https://www.google.com", timeout=5)
            except requests.exceptions.ConnectionError:
                await asyncio.sleep(5)
                continue

            try:
                response = requests.get("http://localhost:8080/usage-stats" , timeout=30)
                if response.status_code == 200:
                    upload_response = requests.post(
                        f"{Home.baseUrl}/mostUseApps/",
                        data=response.json(),
                        headers=headers,
                    )
                    if upload_response.status_code == 200:
                        print("✅ تم رفع الصورة بنجاح")
                    else:
                        print(f"⚠️ خطأ أثناء رفع الصورة: {upload_response.text}")
                else:
                    print("❌ لم يتم التقاط لقطة الشاشة بنجاح")

            except requests.exceptions.RequestException as e:
                print(f"⚠️ خطأ في الطلب: {e}")

            if not self.UsageStatsState:
                break

            await asyncio.sleep(5)

    # دالة عرض رسالة للمستخدم
    # تقوم بعرض رسالة (SnackBar) للمستخدم
    def showMessage(self, message):
        snack_bar = SnackBar(
            content=Text(
                f"{message}",
                style=TextStyle(size=15, font_family="ElMessiri"),  # تنسيق النص
            ),
            show_close_icon=True,  # إظهار زر الإغلاق
        )
        self.page.open(snack_bar)  # عرض الرسالة

    # دالة بدء أو إيقاف مراقبة الشاشة
    # تقوم بتفعيل أو إيقاف مراقبة الشاشة بناءً على حالة التبديل
    def startGetScreenShot(self, stateus):
        def start(self):
            if stateus.data == "true":
                if not self.screenShotState:
                    self.page.client_storage.set("screenShotState", True)
                    self.screenShotState = True
                    self.page.run_task(self.getBackground)
                    self.showMessage("✅ تم البدء في التقاط الشاشة")
            else:
                self.screenShotState = False
                self.page.client_storage.set("screenShotState", False)
                self.showMessage("⏹️ تم إيقاف التقاط الشاشة")

        if self.page.client_storage.contains_key("screenShotState"):
            start(self)
        else:
            self.page.client_storage.set("screenShotState", True)
            start(self)

    # دالة بدء أو إيقاف مراقبة استخدام التطبيقات
    # تقوم بتفعيل أو إيقاف مراقبة استخدام التطبيقات بناءً على حالة التبديل
    def startGetUsageStats(self, stateus):
        def start(self):
            if stateus.data == "true":
                if not self.UsageStatsState:
                    self.UsageStatsState = True
                    self.page.client_storage.set("UsageStatsState", True)
                    self.page.run_task(self.getUsageStats)
                    self.showMessage("✅ تم البدء في مراقبة التطبقات ")
            else:
                self.UsageStatsState = False
                self.page.client_storage.set("UsageStatsState", False)
                self.showMessage("⏹️ تم إيقاف  مراقبة التطبيقات")

        if self.page.client_storage.contains_key("UsageStatsState"):
            start(self)
        else:
            self.page.client_storage.set("UsageStatsState", True)
            start(self)

    # دالة عرض واجهة التحميل
    # تعرض واجهة تحميل (ProgressRing) أثناء انتظار اكتمال المهام
    def loaderUi(self):
        self.scroll = None
        self.controls.clear()
        self.controls.append(
            Column(
                controls=[
                    Container(
                        content=ProgressRing(visible=True),  # حلقة التقدم
                        alignment=alignment.center,  # محاذاة الحلقة في المنتصف
                        height=float("inf"),  # جعل الحاوية تأخذ الارتفاع الكامل
                        expand=True,  # توسيع الحاوية لملء المساحة المتاحة
                    ),
                ],
                expand=True,  # توسيع العمود لملء المساحة المتاحة
            )
        )
        self.update()  # تحديث الواجهة

    # دالة التعامل مع تغيير العنصر المحدد في القائمة الجانبية
    # تقوم بالانتقال إلى الصفحة المحددة أو تسجيل الخروج
    def handle_change(self, e):
        routs = {
            "0": "/home",
            "1": "/",
        }
        if routs[e.data] == "/":
            self.page.client_storage.clear()  # مسح التخزين المحلي
        self.page.go(routs[e.data])  # الانتقال إلى الصفحة المحددة
        self.page.close(self.drawer)  # إغلاق القائمة الجانبية

    # دالة التحقق من وجود أب مرتبط
    # تقوم بالتحقق من وجود أب مرتبط وعرض الواجهة المناسبة
    def checkIsThereFather(self):
        state, _ = self.page.run_task(self.sendHeadRequest, "Children").result()
        if not state:
            userData = self.page.client_storage.get("userData")
            self.hasNoFather(userData)  # عرض واجهة بدون أب
        else:
            userData = self.page.client_storage.get("userData")
            self.hasFatherScreen(userData)  # عرض واجهة مع أب

    # دالة التحقق المستمر من وجود أب مرتبط
    # تقوم بالتحقق بشكل دوري من وجود أب مرتبط وتحديث الواجهة
    async def checkIsTherFatherLoop(self):
        while self.checkIsThereFatherVar:
            await asyncio.sleep(10)
            state, result = await self.sendHeadRequest("Children")
            if not self.checkIsThereFatherVar:
                break
            if state:
                userData = await self.page.client_storage.get_async("userData")
                self.hasFatherScreen(userData)
            else:
                self.screenShotState = False  # إيقاف مراقبة الشاشة
                self.UsageStatsState = False  # إيقاف مراقبة استخدام التطبيقات
                await self.page.client_storage.set_async("UsageStatsState", False)
                await self.page.client_storage.set_async("screenShotState", False)
                userData = await self.page.client_storage.get_async("userData")
                self.hasNoFather(userData)

    # دالة يتم تنفيذها عند إغلاق الصفحة
    # تقوم بإيقاف جميع المهام وإعادة تعيين الحالات
    def will_unmount(self):
        self.screenShotState = False  # إيقاف مراقبة الشاشة
        self.UsageStatsState = False  # إيقاف مراقبة استخدام التطبيقات
        self.checkIsThereFatherVar = False  # إيقاف التحقق المستمر من وجود أب