from flet import *
import requests

class Login(View):
    def __init__(self, route, page):
        super().__init__(
            route=route
        )  # استدعاء مُنشئ الفئة الأم (View)
        self.rtl = True  # تمكين النص من اليمين إلى اليسار للغة العربية

        self.scroll = ScrollMode.AUTO  # تمكين التمرير التلقائي
        # إنشاء حقل إدخال اسم المستخدم مع التنسيق وخيارات التحقق
        self.userNameTextBox = TextField(
            label="اســـم المــستخدم",  # تسمية الحقل بالعربية
            border_radius=border_radius.all(22),  # حواف مستديرة للحقل
            border_color="#171335",  # لون الحواف
            text_style=TextStyle(
                size=15, font_family="ElMessiri"
            ),  # تنسيق النص المدخل
            label_style=TextStyle(
                size=18, font_family="ElMessiri"
            ),  # تنسيق تسمية الحقل
        )

        # إنشاء حقل إدخال كلمة المرور مع خيار إظهار/إخفاء كلمة المرور والتنسيق
        self.passwordTextBox = TextField(
            label="كــلمة المــرور",  # تسمية الحقل بالعربية
            password=True,  # جعل الحقل خاصًا بإدخال كلمة المرور
            can_reveal_password=True,  # إمكانية إظهار/إخفاء كلمة المرور
            border_radius=border_radius.all(22),  # حواف مستديرة للحقل
            border_color="#171335",  # لون الحواف
            text_style=TextStyle(
                size=15, font_family="ElMessiri"
            ),  # تنسيق النص المدخل
            label_style=TextStyle(
                size=18, font_family="ElMessiri"
            ),  # تنسيق تسمية الحقل
        )

    def did_mount(self):
        self.loginUi()  # استدعاء واجهة تسجيل الدخول عند تحميل الصفحة

    def loginUi(self):
        self.scroll = ScrollMode.AUTO  # تمكين التمرير التلقائي
        self.controls.clear()  # مسح العناصر الحالية في الواجهة
        self.controls.append(
            ResponsiveRow(
                controls=[
                    Row(
                        controls=[
                            # زر العودة للصفحة السابقة
                            IconButton(
                                icon=icons.ARROW_BACK,
                                on_click=lambda x: self.page.go("/"),
                            )
                        ],
                        expand=False,
                        alignment=MainAxisAlignment.START,  # محاذاة الزر إلى اليسار
                    ),
                    Column(
                        controls=[
                            # صورة الشعار في أعلى واجهة تسجيل الدخول
                            ResponsiveRow(
                                controls=[
                                    Image(
                                        src="/images/logo.png",  # مسار صورة الشعار
                                        fit=ImageFit.COVER,  # طريقة عرض الصورة
                                        border_radius=border_radius.all(
                                            20.0
                                        ),  # حواف مستديرة للصورة
                                        col={
                                            "xs": 10,
                                            "sm": 10,
                                            "md": 7,
                                            "lg": 5,
                                            "xl": 5,
                                        },
                                    ),
                                ],
                                expand=False,
                                alignment=MainAxisAlignment.CENTER,  # محاذاة الصورة في المنتصف
                            ),
                            # نص العنوان في أعلى الواجهة
                            Text(
                                "حماية الاطفال",  # العنوان بالعربية
                                size=20,
                                weight=FontWeight.BOLD,
                                font_family="ElMessiri",
                            ),
                            Container(height=10),  # مسافة بين العناصر
                            self.userNameTextBox,  # حقل إدخال اسم المستخدم
                            Container(height=10),  # مسافة بين العناصر
                            self.passwordTextBox,  # حقل إدخال كلمة المرور
                            Container(height=20),  # مسافة بين العناصر
                            ResponsiveRow(
                                controls=[
                                    # زر تسجيل الدخول
                                    ElevatedButton(
                                        "تسجيل الدخول",  # نص الزر بالعربية
                                        style=ButtonStyle(
                                            shape=RoundedRectangleBorder(
                                                radius=22
                                            ),  # حواف مستديرة للزر
                                            bgcolor="#171335",  # لون خلفية الزر
                                            color="#ffffff",  # لون نص الزر
                                            text_style=TextStyle(
                                                size=15,
                                                weight=FontWeight.BOLD,
                                                font_family="ElMessiri",  # تنسيق نص الزر
                                            ),
                                            padding=5,  # الحشو الداخلي للزر
                                        ),
                                        on_click=lambda e: self.LoginEvent(),  # حدث النقر على الزر
                                    ),
                                ]
                            ),
                        ],
                        horizontal_alignment=CrossAxisAlignment.CENTER,  # محاذاة العناصر في المنتصف
                        alignment=MainAxisAlignment.CENTER,  # محاذاة العناصر في المنتصف
                    ),
                ],
                expand=True,  # توسيع الصف لملء المساحة المتاحة
            )
        )
        self.update()  # تحديث الواجهة

    # وظيفة لإنشاء واجهة التحميل (حلقة التقدم)
    def loaderUi(self):
        self.scroll = None  # تعطيل التمرير
        return Column(
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

    def checkTextBoxes(self):
        if not self.userNameTextBox.value:  # التحقق من أن حقل اسم المستخدم غير فارغ
            self.userNameTextBox.error = Text(
                "الرجاء ادخال اسم المستخدم"
            )  # عرض رسالة خطأ
            self.update()  # تحديث الواجهة لعرض الخطأ
            return False
        elif not self.passwordTextBox.value:  # التحقق من أن حقل كلمة المرور غير فارغ
            self.passwordTextBox.error = Text(
                "الرجاء ادخال كلمة المرور "
            )  # عرض رسالة خطأ
            self.update()
            return False
        else:
            self.userNameTextBox.error = (
                None  # إزالة أي رسالة خطأ من حقل اسم المستخدم
            )
            self.passwordTextBox.error = (
                None  # إزالة أي رسالة خطأ من حقل كلمة المرور
            )
            self.update()
            return True

    async def loginRequest(self, userName, password):
        body = {"username": userName, "password": password , "userType": 1}  # بيانات الطلب
        try:
            response = requests.post(url=f"{Login.baseUrl}/login/", data=body)  # إرسال الطلب
            json = response.json()  # تحويل الاستجابة إلى JSON
            if response.status_code == 200:  # إذا كانت الاستجابة ناجحة
                await self.page.client_storage.set_async("access", json["access"])  # حفظ رمز الوصول
                await self.page.client_storage.set_async("refresh", json["refresh"])  # حفظ رمز التحديث
                userData = {
                    "username":json["username"],
                    "gender":json["gender"],
                    "first_name":json["first_name"],
                    "last_name":json["last_name"],
                    "profileImage":json["profileImage"],
                    "key":json["key"],
                    "father_first_name":json["father_first_name"],
                    "father_last_name":json["father_last_name"],
                    "father_gender":json["father_gender"],
                } if json.get("father_first_name") else {
                    "username":json["username"],
                    "gender":json["gender"],
                    "first_name":json["first_name"],
                    "last_name":json["last_name"],
                    "profileImage":json["profileImage"],
                    "key":json["key"],
                }
                await self.page.client_storage.set_async("userData", userData)  # حفظ بيانات المستخدم
                return [True, json]  # إرجاع النتيجة الناجحة
            else:
                return [False, json["non_field_errors"][0]]  # إرجاع رسالة الخطأ
        except requests.exceptions.Timeout:
            return [False, "اتصال الانترنت بطئ"]  # إرجاع رسالة خطأ في حالة انتهاء المهلة
        except requests.exceptions.ConnectionError:
            return [False, "حدث خطأ في الاتصال بالخادم. تحقق من اتصالك بالإنترنت."]  # إرجاع رسالة خطأ في حالة فشل الاتصال

    # وظيفة التعامل مع حدث تسجيل الدخول
    def LoginEvent(self):
        if self.checkTextBoxes():  # التحقق من صحة الحقول
            self.controls.clear()  # مسح العناصر الحالية
            self.controls.append(self.loaderUi())  # عرض واجهة التحميل
            self.update()  # تحديث الواجهة
            # محاكاة طلب تسجيل الدخول
            authState = self.page.run_task(
                self.loginRequest,
                self.userNameTextBox.value,
                self.passwordTextBox.value,
            ).result()
            if authState[0]:  # إذا كان تسجيل الدخول ناجحًا
                self.page.go("/home")  # الانتقال إلى الصفحة الرئيسية
            else:  # إذا فشل تسجيل الدخول
                self.controls.clear()  # مسح العناصر الحالية
                self.loginUi()  # إعادة عرض واجهة تسجيل الدخول
                snack_bar = SnackBar(
                    content=Text(
                        f"{authState[1]}",  # عرض رسالة الخطأ
                        style=TextStyle(size=15, font_family="ElMessiri"),
                    ),
                    show_close_icon=True,  # إظهار زر الإغلاق
                )
                self.page.open(snack_bar)  # عرض رسالة الخطأ
                self.update()  # تحديث الواجهة