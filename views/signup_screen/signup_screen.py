from flet import *
import requests

class SignUp(View):
    def __init__(self, route, page):
        super().__init__(route=route)  # استدعاء مُنشئ الفئة الأم (View)
        self.scroll = ScrollMode.AUTO  # تمكين التمرير التلقائي

        # إنشاء حقل إدخال الاسم الأول مع التنسيق
        self.firstNameTextBox = TextField(
            label="الاسم الاول",  # تسمية الحقل بالعربية
            border_radius=border_radius.all(22),  # حواف مستديرة للحقل
            border_color="#171335",  # لون الحواف
            text_style=TextStyle(size=15, font_family="ElMessiri"),  # تنسيق النص المدخل
            label_style=TextStyle(size=14, font_family="ElMessiri"),  # تنسيق تسمية الحقل
        )

        # إنشاء حقل إدخال الاسم الأخير مع التنسيق
        self.lastNameTextBox = TextField(
            label="الاسم الاخير",  # تسمية الحقل بالعربية
            border_radius=border_radius.all(22),  # حواف مستديرة للحقل
            border_color="#171335",  # لون الحواف
            text_style=TextStyle(size=15, font_family="ElMessiri"),  # تنسيق النص المدخل
            label_style=TextStyle(size=14, font_family="ElMessiri"),  # تنسيق تسمية الحقل
        )

        # إنشاء حقل إدخال اسم المستخدم مع التنسيق
        self.userNameTextBox = TextField(
            label="اســـم المــستخدم",  # تسمية الحقل بالعربية
            border_radius=border_radius.all(22),  # حواف مستديرة للحقل
            border_color="#171335",  # لون الحواف
            text_style=TextStyle(size=15, font_family="ElMessiri"),  # تنسيق النص المدخل
            label_style=TextStyle(size=14, font_family="ElMessiri"),  # تنسيق تسمية الحقل
        )

        # إنشاء قائمة اختيار الجنس مع التنسيق
        self.genderOptionMenu = Dropdown(
            label="الجنس",  # تسمية القائمة بالعربية
            width=100,  # عرض القائمة
            options=[
                dropdown.Option(content=Text("ذكر"), text=1),  # خيار "ذكر"
                dropdown.Option(content=Text("انثى"), text=2),  # خيار "أنثى"
            ],
            label_style=TextStyle(
                size=13,
                weight=FontWeight.NORMAL,
                font_family="ElMessiri",  # تنسيق تسمية القائمة
            ),
            border_radius=border_radius.all(22),  # حواف مستديرة للقائمة
        )

        # إنشاء حقل إدخال كلمة المرور مع التنسيق
        self.passwordTextBox = TextField(
            label="كــلمة المــرور",  # تسمية الحقل بالعربية
            password=True,  # جعل الحقل خاصًا بإدخال كلمة المرور
            can_reveal_password=True,  # إمكانية إظهار/إخفاء كلمة المرور
            border_radius=border_radius.all(22),  # حواف مستديرة للحقل
            border_color="#171335",  # لون الحواف
            text_style=TextStyle(size=15, font_family="ElMessiri"),  # تنسيق النص المدخل
            label_style=TextStyle(size=14, font_family="ElMessiri"),  # تنسيق تسمية الحقل
        )

        # إنشاء حقل إدخال تأكيد كلمة المرور مع التنسيق
        self.rePasswordTextBox = TextField(
            label="تأكيد كــلمة المــرور",  # تسمية الحقل بالعربية
            password=True,  # جعل الحقل خاصًا بإدخال كلمة المرور
            can_reveal_password=True,  # إمكانية إظهار/إخفاء كلمة المرور
            border_radius=border_radius.all(22),  # حواف مستديرة للحقل
            border_color="#171335",  # لون الحواف
            text_style=TextStyle(size=15, font_family="ElMessiri"),  # تنسيق النص المدخل
            label_style=TextStyle(size=14, font_family="ElMessiri"),  # تنسيق تسمية الحقل
        )

        self.content = self.SignUpUi()  # إنشاء واجهة التسجيل
        self.controls.append(self.content)  # إضافة الواجهة إلى عناصر التحكم

    def SignUpUi(self):
        self.scroll = ScrollMode.AUTO  # تمكين التمرير التلقائي
        return ResponsiveRow(
            controls=[
                Row(
                    controls=[
                        # زر العودة للصفحة السابقة
                        IconButton(
                            icon=icons.ARROW_BACK, on_click=lambda x: self.page.go("/")
                        )
                    ],
                    expand=False,
                    alignment=MainAxisAlignment.START,  # محاذاة الزر إلى اليسار
                ),
                Column(
                    controls=[
                        # صورة الشعار في أعلى واجهة التسجيل
                        ResponsiveRow(
                            controls=[
                                Image(
                                    src="images/logo.png",  # مسار صورة الشعار
                                    fit=ImageFit.COVER,  # طريقة عرض الصورة
                                    border_radius=border_radius.all(20.0),  # حواف مستديرة للصورة
                                    col={"xs": 10, "sm": 10, "md": 7, "lg": 5, "xl": 5},
                                ),
                            ],
                            expand=False,
                            alignment=MainAxisAlignment.CENTER,  # محاذاة الصورة في المنتصف
                        ),
                        Container(height=5),  # مسافة بين العناصر
                        # نص العنوان في أعلى الواجهة
                        Text(
                            "حماية الاطفال",  # العنوان بالعربية
                            size=20,
                            weight=FontWeight.BOLD,
                            font_family="ElMessiri",
                        ),
                        ResponsiveRow(
                            controls=[self.firstNameTextBox],  # حقل الاسم الأول
                        ),
                        Container(height=5),  # مسافة بين العناصر
                        ResponsiveRow(
                            controls=[self.lastNameTextBox],  # حقل الاسم الأخير
                        ),
                        Container(height=5),  # مسافة بين العناصر
                        ResponsiveRow(
                            controls=[self.genderOptionMenu],  # قائمة اختيار الجنس
                        ),
                        Container(height=5),  # مسافة بين العناصر
                        self.userNameTextBox,  # حقل اسم المستخدم
                        Container(height=5),  # مسافة بين العناصر
                        self.passwordTextBox,  # حقل كلمة المرور
                        Container(height=5),  # مسافة بين العناصر
                        self.rePasswordTextBox,  # حقل تأكيد كلمة المرور
                        Container(height=20),  # مسافة بين العناصر
                        ResponsiveRow(
                            controls=[
                                # زر إنشاء الحساب
                                ElevatedButton(
                                    "انــشاء حــساب",  # نص الزر بالعربية
                                    style=ButtonStyle(
                                        shape=RoundedRectangleBorder(radius=22),  # حواف مستديرة للزر
                                        bgcolor="#171335",  # لون خلفية الزر
                                        color="#ffffff",  # لون نص الزر
                                        text_style=TextStyle(
                                            size=15,
                                            weight=FontWeight.BOLD,
                                            font_family="ElMessiri",  # تنسيق نص الزر
                                        ),
                                        padding=5,  # الحشو الداخلي للزر
                                    ),
                                    on_click=lambda e: self.SignUpEvent(),  # حدث النقر على الزر
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

    def checkTextBoxData(self):
        # التحقق من صحة البيانات المدخلة في الحقول
        errors = [
            True if self.firstNameTextBox.value != "" else "الرجاء ادخال اسمك الاول",
            True if self.lastNameTextBox.value != "" else "الرجاء ادخال اسمك الاخير",
            True if self.genderOptionMenu.value != None else "الرجاء اختيار الجنس",
            (
                True
                if len(self.userNameTextBox.value) > 2
                and self.userNameTextBox.value != ""
                else "يجب ان يتكون اسم المستخدم من 3 احرف على الاقل"
            ),
            (
                True
                if len(self.passwordTextBox.value) > 5
                and self.passwordTextBox.value != ""
                else "يجب ان تتكون كلمة المرور  من 6 احرف على الاقل"
            ),
            (
                True
                if self.rePasswordTextBox.value != ""
                else "الرجاء ادخال تاكيد كلمة المرور"
            ),
            (
                True
                if self.passwordTextBox.value == self.rePasswordTextBox.value
                else "كلمة المرور غير متطابقة"
            ),
        ]

        textBoxes = [
            self.firstNameTextBox,
            self.lastNameTextBox,
            self.genderOptionMenu,
            self.userNameTextBox,
            self.passwordTextBox,
            self.rePasswordTextBox,
            self.rePasswordTextBox,
        ]
        state = True
        for index, error in enumerate(errors):
            if error != True:
                state = False
                textBoxes[index].error = Text(f"{error}")  # عرض رسالة الخطأ
            else:
                textBoxes[index].error = None  # إزالة رسالة الخطأ
        self.update()
        textBoxes.pop()
        return [[text.value for text in textBoxes], state]  # إرجاع البيانات وحالة التحقق

    async def SignUpRequest(self, data):
        # إرسال طلب إنشاء حساب إلى الخادم
        body = {
            "first_name": data[0],
            "last_name": data[1],
            "gender": data[2],
            "username": data[3],
            "password": data[4],
            "userType": 1,
        }
        try:
            response = requests.post(url=f"{SignUp.baseUrl}/signup/", data=body)  # إرسال الطلب
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
                }
                await self.page.client_storage.set_async("userData", userData)  # حفظ بيانات المستخدم
                return [True, "تم تسجيل الدخول بنجاح"]  # إرجاع النتيجة الناجحة
            else:
                return [False, json["username"][0]]  # إرجاع رسالة الخطأ
        except requests.exceptions.Timeout:
            return [False, "اتصال الانترنت بطئ"]  # إرجاع رسالة خطأ في حالة انتهاء المهلة
        except requests.exceptions.ConnectionError:
            return [False, "حدث خطأ في الاتصال بالخادم. تحقق من اتصالك بالإنترنت."]  # إرجاع رسالة خطأ في حالة فشل الاتصال

    def SignUpEvent(self):
        data, state = self.checkTextBoxData()  # التحقق من صحة البيانات
        if state:
            self.controls.clear()  # مسح العناصر الحالية
            self.controls.append(self.loaderUi())  # عرض واجهة التحميل
            self.update()  # تحديث الواجهة
            authState = self.page.run_task(self.SignUpRequest , data).result()  # إرسال طلب التسجيل
            if authState[0]:  # إذا كان التسجيل ناجحًا
                self.page.go("/home")  # الانتقال إلى الصفحة الرئيسية
            else:  # إذا فشل التسجيل
                self.controls.clear()  # مسح العناصر الحالية
                self.controls.append(self.SignUpUi())  # إعادة عرض واجهة التسجيل
                snack_bar = SnackBar(
                    content=Text(
                        f"{authState[1]}",  # عرض رسالة الخطأ
                        style=TextStyle(size=15, font_family="ElMessiri"),
                    ),
                    show_close_icon=True,  # إظهار زر الإغلاق
                )
                self.page.open(snack_bar)  # عرض رسالة الخطأ
                self.update()  # تحديث الواجهة