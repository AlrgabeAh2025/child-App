from flet import *
import requests


class PersonalInformation(View):
    # دالة البناء (Constructor)
    # تهيئة الكلاس وتعيين المتغيرات الأولية
    def __init__(self, route, page):
        super().__init__(route=route)  # استدعاء مُنشئ الفئة الأم (View)
        self.scroll = ScrollMode.AUTO  # تمكين التمرير التلقائي
        self.page = page  # تعيين الصفحة الحالية

        # إنشاء شريط التطبيق (AppBar)
        self.appbar = AppBar(
            leading=IconButton(
                icon=icons.ARROW_BACK,  # أيقونة العودة
                icon_color="#ffffff",  # لون الأيقونة
                on_click=lambda x: self.page.go(
                    "/Profile"
                ),  # حدث النقر للعودة إلى الملف الشخصي
            ),
            title=Text(
                "حماية الاطفال",  # عنوان شريط التطبيق
                size=20,
                weight=FontWeight.BOLD,
                color="#ffffff",  # لون النص
                font_family="ElMessiri",  # نوع الخط
            ),
            toolbar_height=100,  # ارتفاع شريط التطبيق
        )

        # إنشاء مراجع لحقول إدخال النص
        self.userName = Ref[TextField]()  # مرجع لحقل اسم المستخدم
        self.firstName = Ref[TextField]()  # مرجع لحقل الاسم الأول
        self.lastName = Ref[TextField]()  # مرجع لحقل الاسم الأخير

    # دالة بناء واجهة المستخدم
    # تقوم ببناء واجهة تعديل المعلومات الشخصية
    def buildUi(self):
        self.controls.clear()  # مسح العناصر الحالية
        userData = self.page.client_storage.get(
            "userData"
        )  # الحصول على بيانات المستخدم
        self.controls.append(
            ResponsiveRow(
                controls=[
                    Column(
                        controls=[
                            Container(
                                content=Image(
                                    src=f"{PersonalInformation.baseUrl}{userData['profileImage']}",  # عرض صورة الملف الشخصي
                                    width=250,  # عرض الصورة
                                ),
                                border_radius=border_radius.all(
                                    150
                                ),  # حواف مستديرة للصورة
                                width=200,  # عرض الحاوية
                                height=200,  # ارتفاع الحاوية
                                border=border.all(
                                    width=0.5, color="black"
                                ),  # إطار الحاوية
                            ),
                            Container(height=20),  # مسافة بين العناصر
                            ResponsiveRow(
                                controls=[
                                    Text(
                                        "تعديل المعلومات الشخصية",  # نص العنوان
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
                            Container(height=10),  # مسافة بين العناصر
                            ResponsiveRow(
                                controls=[
                                    TextField(
                                        label="اسم المستخدم",  # تسمية الحقل
                                        border_radius=border_radius.all(
                                            22
                                        ),  # حواف مستديرة للحقل
                                        border_color="#171335",  # لون الحواف
                                        text_style=TextStyle(
                                            size=15,
                                            font_family="ElMessiri",  # تنسيق النص
                                        ),
                                        label_style=TextStyle(
                                            size=14,
                                            font_family="ElMessiri",  # تنسيق التسمية
                                        ),
                                        ref=self.userName,  # تعيين المرجع
                                        value=userData[
                                            "username"
                                        ],  # تعيين القيمة الافتراضية
                                    ),
                                ],
                            ),
                            Container(height=10),  # مسافة بين العناصر
                            ResponsiveRow(
                                controls=[
                                    TextField(
                                        label="الاسم الاول",  # تسمية الحقل
                                        border_radius=border_radius.all(
                                            22
                                        ),  # حواف مستديرة للحقل
                                        border_color="#171335",  # لون الحواف
                                        text_style=TextStyle(
                                            size=15,
                                            font_family="ElMessiri",  # تنسيق النص
                                        ),
                                        label_style=TextStyle(
                                            size=14,
                                            font_family="ElMessiri",  # تنسيق التسمية
                                        ),
                                        ref=self.firstName,  # تعيين المرجع
                                        value=userData[
                                            "first_name"
                                        ],  # تعيين القيمة الافتراضية
                                    ),
                                ],
                            ),
                            Container(height=10),  # مسافة بين العناصر
                            ResponsiveRow(
                                controls=[
                                    TextField(
                                        label="الاسم الاخير",  # تسمية الحقل
                                        border_radius=border_radius.all(
                                            22
                                        ),  # حواف مستديرة للحقل
                                        border_color="#171335",  # لون الحواف
                                        text_style=TextStyle(
                                            size=15,
                                            font_family="ElMessiri",  # تنسيق النص
                                        ),
                                        label_style=TextStyle(
                                            size=14,
                                            font_family="ElMessiri",  # تنسيق التسمية
                                        ),
                                        ref=self.lastName,  # تعيين المرجع
                                        value=userData[
                                            "last_name"
                                        ],  # تعيين القيمة الافتراضية
                                    ),
                                ],
                            ),
                            Container(height=10),  # مسافة بين العناصر
                            ResponsiveRow(
                                controls=[
                                    ElevatedButton(
                                        "حفظ التعديلات",  # نص الزر
                                        style=ButtonStyle(
                                            shape=RoundedRectangleBorder(
                                                radius=22
                                            ),  # حواف مستديرة للزر
                                            bgcolor="#171335",  # لون خلفية الزر
                                            color="#ffffff",  # لون النص
                                            text_style=TextStyle(
                                                size=15,
                                                weight=FontWeight.BOLD,
                                                font_family="ElMessiri",  # تنسيق النص
                                            ),
                                            padding=5,  # الحشو الداخلي
                                        ),
                                        on_click=self.changeData,  # حدث النقر على الزر
                                    ),
                                ]
                            ),
                        ],
                        horizontal_alignment=CrossAxisAlignment.CENTER,  # محاذاة العناصر في المنتصف
                        alignment=MainAxisAlignment.CENTER,  # محاذاة العناصر في المنتصف
                    )
                ],
                vertical_alignment=CrossAxisAlignment.CENTER,  # محاذاة العناصر في المنتصف
                alignment=alignment.center,  # محاذاة العناصر في المنتصف
            ),
        )
        self.update()  # تحديث الواجهة

    # دالة يتم تنفيذها عند تحميل الصفحة
    # تقوم ببناء واجهة المستخدم
    def did_mount(self):
        self.buildUi()

    # دالة إرسال طلب PATCH لتحديث المعلومات الشخصية
    # تقوم بإرسال البيانات المحدثة إلى الخادم
    async def sendPatchRequest(self, url, body={}):
        body = {
            "action": "updatePersonaInfo",  # نوع الإجراء
            "username": f"{body[0]}",  # اسم المستخدم
            "first_name": f"{body[1]}",  # الاسم الأول
            "last_name": f"{body[2]}",  # الاسم الأخير
        }
        access = await self.page.client_storage.get_async(
            "access"
        )  # الحصول على رمز الوصول
        headers = {
            "Authorization": f"Bearer {access}",
            "Accept": "*/*",
            "Cache-Control": "no-cache",
        }
        try:
            response = requests.patch(
                url=f"{PersonalInformation.baseUrl}/{url}/", data=body, headers=headers
            )
            json = response.json()  # تحويل الاستجابة إلى JSON
            if response.status_code == 200:
                return [True, json]  # إرجاع النتيجة الناجحة
            else:
                return [False, json]  # إرجاع النتيجة الفاشلة
        except requests.exceptions.Timeout:
            return [
                False,
                "اتصال الانترنت بطئ",
            ]  # إرجاع رسالة خطأ في حالة انتهاء المهلة
        except requests.exceptions.ConnectionError:
            return [
                False,
                "حدث خطأ في الاتصال بالخادم. تحقق من اتصالك بالإنترنت.",
            ]  # إرجاع رسالة خطأ في حالة فشل الاتصال

    # دالة عرض واجهة الخطأ
    # تعرض رسالة خطأ مع زر لإعادة المحاولة
    def ErrorUi(self):
        self.scroll = None
        self.controls.clear()
        self.controls.append(
            Column(
                controls=[
                    Container(
                        content=Text(
                            "حدث خطأ الرجاء اعادة المحاولة",  # نص الخطأ
                            style=TextStyle(
                                size=15,
                                weight=FontWeight.BOLD,
                                font_family="ElMessiri",  # تنسيق النص
                            ),
                        ),
                        alignment=alignment.center,  # محاذاة النص في المنتصف
                        expand=True,  # توسيع الحاوية لملء المساحة المتاحة
                    ),
                    Container(
                        content=TextButton(
                            icon=icons.REPLAY_OUTLINED,  # أيقونة إعادة المحاولة
                            text="اعادة المحاولة",  # نص الزر
                            style=ButtonStyle(
                                text_style=TextStyle(
                                    size=15,
                                    weight=FontWeight.BOLD,
                                    font_family="ElMessiri",  # تنسيق النص
                                ),
                            ),
                            on_click=lambda e: self.did_mount(),  # حدث النقر على الزر
                        ),
                        alignment=alignment.center,  # محاذاة الزر في المنتصف
                    ),
                ],
                expand=True,  # توسيع العمود لملء المساحة المتاحة
            )
        )
        self.update()  # تحديث الواجهة

    # دالة عرض واجهة التحميل
    # تعرض حلقة تحميل أثناء انتظار اكتمال المهام
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

    # دالة التحقق من صحة البيانات المدخلة
    # تقوم بالتحقق من أن الحقول غير فارغة وتعيد البيانات وحالة التحقق
    def checkTextBoxData(self):
        errors = [
            (
                True
                if self.userName.current.value != ""
                else "الرجاء ادخال اسم المستخدم"
            ),  # التحقق من اسم المستخدم
            (
                True
                if self.firstName.current.value != ""
                else "الرجاء ادخال اسمك الاول"
            ),  # التحقق من الاسم الأول
            (
                True
                if self.lastName.current.value != ""
                else "الرجاء ادخال اسمك الاخير"
            ),  # التحقق من الاسم الأخير
            (
                True
                if len(self.userName.current.value) > 2
                and self.userName.current.value != ""
                else "يجب ان يتكون اسم المستخدم من 3 احرف على الاقل"  # التحقق من طول اسم المستخدم
            ),
        ]
        textBoxes = [
            self.userName,
            self.firstName,
            self.lastName,
            self.userName,
        ]
        state = True
        for index, error in enumerate(errors):
            if error != True:
                state = False
                textBoxes[index].current.error = Text(f"{error}")  # عرض رسالة الخطأ
            else:
                textBoxes[index].current.error = None  # إزالة رسالة الخطأ
        self.update()
        textBoxes.pop()
        return [
            [text.current.value for text in textBoxes],
            state,
        ]  # إرجاع البيانات وحالة التحقق

    # دالة عرض رسالة للمستخدم
    # تعرض رسالة (SnackBar) للمستخدم
    def showMessage(self, message):
        snack_bar = SnackBar(
            content=Text(
                f"{message}",
                style=TextStyle(size=15, font_family="ElMessiri"),  # تنسيق النص
            ),
            show_close_icon=True,  # إظهار زر الإغلاق
        )
        self.page.open(snack_bar)  # عرض الرسالة

    # دالة تحديث بيانات المستخدم
    # تقوم بتحديث بيانات المستخدم في التخزين المحلي
    def updateUserData(self, result):
        userData = {
            "username": result["username"],
            "gender": result["gender"],
            "first_name": result["first_name"],
            "last_name": result["last_name"],
            "profileImage": result["profileImage"],
        }
        self.page.client_storage.set("userData", userData)  # تحديث بيانات المستخدم

    # دالة تغيير البيانات الشخصية
    # تقوم بالتحقق من البيانات وإرسالها إلى الخادم للتحديث
    def changeData(self, e):
        values, textBoxState = self.checkTextBoxData()  # التحقق من صحة البيانات
        if textBoxState:
            self.loaderUi()  # عرض واجهة التحميل
            state, result = self.page.run_task(
                self.sendPatchRequest, "updateUser", values
            ).result()
            if state:
                self.updateUserData(result)  # تحديث بيانات المستخدم
                self.showMessage("تم تحديث البيانات بنجاح")  # عرض رسالة نجاح
                self.did_mount()  # إعادة بناء الواجهة
            else:
                self.did_mount()  # إعادة بناء الواجهة
                self.showMessage(result)  # عرض رسالة الخطأ


class SecurityPasswords(View):
    # دالة البناء (Constructor)
    # تهيئة الكلاس وتعيين المتغيرات الأولية
    def __init__(self, route, page):
        super().__init__(route=route)  # استدعاء مُنشئ الفئة الأم (View)
        self.scroll = ScrollMode.AUTO  # تمكين التمرير التلقائي
        self.page = page  # تعيين الصفحة الحالية

        # إنشاء شريط التطبيق (AppBar)
        self.appbar = AppBar(
            leading=IconButton(
                icon=icons.ARROW_BACK,  # أيقونة العودة
                icon_color="#ffffff",  # لون الأيقونة
                on_click=lambda x: self.page.go(
                    "/Profile"
                ),  # حدث النقر للعودة إلى الملف الشخصي
            ),
            title=Text(
                "حماية الاطفال",  # عنوان شريط التطبيق
                size=20,
                weight=FontWeight.BOLD,
                color="#ffffff",  # لون النص
                font_family="ElMessiri",  # نوع الخط
            ),
            toolbar_height=100,  # ارتفاع شريط التطبيق
        )

        # إنشاء مراجع لحقول إدخال النص
        self.currentPassword = Ref[TextField]()  # مرجع لحقل كلمة المرور الحالية
        self.newPassword = Ref[TextField]()  # مرجع لحقل كلمة المرور الجديدة
        self.newRePassword = Ref[TextField]()  # مرجع لحقل تأكيد كلمة المرور الجديدة

    # دالة بناء واجهة المستخدم
    # تقوم ببناء واجهة تغيير كلمة المرور
    def buildUi(self):
        self.controls.clear()  # مسح العناصر الحالية
        self.controls.append(
            ResponsiveRow(
                controls=[
                    Column(
                        controls=[
                            Container(height=10),  # مسافة بين العناصر
                            ResponsiveRow(
                                controls=[
                                    Text(
                                        "تغيير كلمة مرور حسابك",  # نص العنوان
                                        style=TextStyle(
                                            size=12,
                                            weight=FontWeight.BOLD,
                                            font_family="ElMessiri",  # تنسيق النص
                                        ),
                                        color="#666666",  # لون النص
                                        text_align=TextAlign.START,  # محاذاة النص
                                    ),
                                ],
                            ),
                            Container(height=10),  # مسافة بين العناصر
                            ResponsiveRow(
                                controls=[
                                    TextField(
                                        label="كلمة المرور الحالية",  # تسمية الحقل
                                        border_radius=border_radius.all(
                                            22
                                        ),  # حواف مستديرة للحقل
                                        border_color="#171335",  # لون الحواف
                                        text_style=TextStyle(
                                            size=15,
                                            font_family="ElMessiri",  # تنسيق النص
                                        ),
                                        label_style=TextStyle(
                                            size=14,
                                            font_family="ElMessiri",  # تنسيق التسمية
                                        ),
                                        password=True,  # جعل الحقل خاصًا بإدخال كلمة المرور
                                        can_reveal_password=True,  # إمكانية إظهار/إخفاء كلمة المرور
                                        ref=self.currentPassword,  # تعيين المرجع
                                    ),
                                ],
                            ),
                            Container(height=10),  # مسافة بين العناصر
                            ResponsiveRow(
                                controls=[
                                    TextField(
                                        label="كلمة المرور الجديدة",  # تسمية الحقل
                                        border_radius=border_radius.all(
                                            22
                                        ),  # حواف مستديرة للحقل
                                        border_color="#171335",  # لون الحواف
                                        text_style=TextStyle(
                                            size=15,
                                            font_family="ElMessiri",  # تنسيق النص
                                        ),
                                        label_style=TextStyle(
                                            size=14,
                                            font_family="ElMessiri",  # تنسيق التسمية
                                        ),
                                        password=True,  # جعل الحقل خاصًا بإدخال كلمة المرور
                                        can_reveal_password=True,  # إمكانية إظهار/إخفاء كلمة المرور
                                        ref=self.newPassword,  # تعيين المرجع
                                    ),
                                ],
                            ),
                            Container(height=10),  # مسافة بين العناصر
                            ResponsiveRow(
                                controls=[
                                    TextField(
                                        label="تأكيد كلمة المرور الحديدة",  # تسمية الحقل
                                        border_radius=border_radius.all(
                                            22
                                        ),  # حواف مستديرة للحقل
                                        border_color="#171335",  # لون الحواف
                                        text_style=TextStyle(
                                            size=15,
                                            font_family="ElMessiri",  # تنسيق النص
                                        ),
                                        label_style=TextStyle(
                                            size=14,
                                            font_family="ElMessiri",  # تنسيق التسمية
                                        ),
                                        password=True,  # جعل الحقل خاصًا بإدخال كلمة المرور
                                        can_reveal_password=True,  # إمكانية إظهار/إخفاء كلمة المرور
                                        ref=self.newRePassword,  # تعيين المرجع
                                    ),
                                ],
                            ),
                            Container(height=10),  # مسافة بين العناصر
                            ResponsiveRow(
                                controls=[
                                    ElevatedButton(
                                        "حفظ التعديلات",  # نص الزر
                                        style=ButtonStyle(
                                            shape=RoundedRectangleBorder(
                                                radius=22
                                            ),  # حواف مستديرة للزر
                                            bgcolor="#171335",  # لون خلفية الزر
                                            color="#ffffff",  # لون النص
                                            text_style=TextStyle(
                                                size=15,
                                                weight=FontWeight.BOLD,
                                                font_family="ElMessiri",  # تنسيق النص
                                            ),
                                            padding=5,  # الحشو الداخلي
                                        ),
                                        on_click=self.updatePassword,  # حدث النقر على الزر
                                    ),
                                ]
                            ),
                        ],
                        horizontal_alignment=CrossAxisAlignment.CENTER,  # محاذاة العناصر في المنتصف
                        alignment=MainAxisAlignment.CENTER,  # محاذاة العناصر في المنتصف
                    )
                ],
                vertical_alignment=CrossAxisAlignment.CENTER,  # محاذاة العناصر في المنتصف
                alignment=alignment.center,  # محاذاة العناصر في المنتصف
            ),
        )
        self.update()  # تحديث الواجهة

    # دالة يتم تنفيذها عند تحميل الصفحة
    # تقوم ببناء واجهة المستخدم
    def did_mount(self):
        self.buildUi()

    # دالة إرسال طلب PATCH لتحديث كلمة المرور
    # تقوم بإرسال البيانات المحدثة إلى الخادم
    async def sendPatchRequest(self, url, body={}):
        body = {
            "action": "updatePassword",  # نوع الإجراء
            "currentPassword": f"{body[0]}",  # كلمة المرور الحالية
            "newPassword": f"{body[1]}",  # كلمة المرور الجديدة
            "rePassword": f"{body[2]}",  # تأكيد كلمة المرور الجديدة
        }
        access = await self.page.client_storage.get_async(
            "access"
        )  # الحصول على رمز الوصول
        headers = {
            "Authorization": f"Bearer {access}",
            "Accept": "*/*",
            "Cache-Control": "no-cache",
        }
        try:
            response = requests.patch(
                url=f"{SecurityPasswords.baseUrl}/{url}/", data=body, headers=headers
            )
            json = response.json()  # تحويل الاستجابة إلى JSON
            if response.status_code == 200:
                return [True, json]  # إرجاع النتيجة الناجحة
            else:
                return [False, json]  # إرجاع النتيجة الفاشلة
        except requests.exceptions.Timeout:
            return [
                False,
                "اتصال الانترنت بطئ",
            ]  # إرجاع رسالة خطأ في حالة انتهاء المهلة
        except requests.exceptions.ConnectionError:
            return [
                False,
                "حدث خطأ في الاتصال بالخادم. تحقق من اتصالك بالإنترنت.",
            ]  # إرجاع رسالة خطأ في حالة فشل الاتصال

    # دالة عرض واجهة الخطأ
    # تعرض رسالة خطأ مع زر لإعادة المحاولة
    def ErrorUi(self):
        self.scroll = None
        self.controls.clear()
        self.controls.append(
            Column(
                controls=[
                    Container(
                        content=Text(
                            "حدث خطأ الرجاء اعادة المحاولة",  # نص الخطأ
                            style=TextStyle(
                                size=15,
                                weight=FontWeight.BOLD,
                                font_family="ElMessiri",  # تنسيق النص
                            ),
                        ),
                        alignment=alignment.center,  # محاذاة النص في المنتصف
                        expand=True,  # توسيع الحاوية لملء المساحة المتاحة
                    ),
                    Container(
                        content=TextButton(
                            icon=icons.REPLAY_OUTLINED,  # أيقونة إعادة المحاولة
                            text="اعادة المحاولة",  # نص الزر
                            style=ButtonStyle(
                                text_style=TextStyle(
                                    size=15,
                                    weight=FontWeight.BOLD,
                                    font_family="ElMessiri",  # تنسيق النص
                                ),
                            ),
                            on_click=lambda e: self.did_mount(),  # حدث النقر على الزر
                        ),
                        alignment=alignment.center,  # محاذاة الزر في المنتصف
                    ),
                ],
                expand=True,  # توسيع العمود لملء المساحة المتاحة
            )
        )
        self.update()  # تحديث الواجهة

    # دالة عرض واجهة التحميل
    # تعرض حلقة تحميل أثناء انتظار اكتمال المهام
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

    # دالة التحقق من صحة البيانات المدخلة
    # تقوم بالتحقق من أن الحقول غير فارغة وتعيد البيانات وحالة التحقق
    def checkTextBoxData(self):
        errors = [
            (
                True
                if self.currentPassword.current.value != ""
                else "الرجاء ادخال كلمة السر الحالية"
            ),  # التحقق من كلمة المرور الحالية
            (
                True
                if self.newPassword.current.value != ""
                else "الرجاء ادخال كلمةالسر الجديدة "
            ),  # التحقق من كلمة المرور الجديدة
            (
                True
                if self.newRePassword.current.value != ""
                else "الرجاء ادخال  تأكيد كلمة المرور الجديدة"
            ),  # التحقق من تأكيد كلمة المرور
            (
                True
                if self.newPassword.current.value == self.newRePassword.current.value
                else "كلمة المرور غير متطابقة"  # التحقق من تطابق كلمتي المرور
            ),
        ]
        textBoxes = [
            self.currentPassword,
            self.newPassword,
            self.newRePassword,
            self.newRePassword,
        ]
        state = True
        for index, error in enumerate(errors):
            if error != True:
                state = False
                textBoxes[index].current.error = Text(f"{error}")  # عرض رسالة الخطأ
            else:
                textBoxes[index].current.error = None  # إزالة رسالة الخطأ
        self.update()
        textBoxes.pop()
        return [
            [text.current.value for text in textBoxes],
            state,
        ]  # إرجاع البيانات وحالة التحقق

    # دالة عرض رسالة للمستخدم
    # تعرض رسالة (SnackBar) للمستخدم
    def showMessage(self, message):
        snack_bar = SnackBar(
            content=Text(
                f"{message}",
                style=TextStyle(size=15, font_family="ElMessiri"),  # تنسيق النص
            ),
            show_close_icon=True,  # إظهار زر الإغلاق
        )
        self.page.open(snack_bar)  # عرض الرسالة

    # دالة تحديث بيانات المستخدم
    # تقوم بتحديث بيانات المستخدم في التخزين المحلي
    def updateUserData(self, result):
        userData = {
            "username": result["username"],
            "gender": result["gender"],
            "first_name": result["first_name"],
            "last_name": result["last_name"],
            "profileImage": result["profileImage"],
        }
        self.page.client_storage.set("userData", userData)  # تحديث بيانات المستخدم

    # دالة تغيير كلمة المرور
    # تقوم بالتحقق من البيانات وإرسالها إلى الخادم لتحديث كلمة المرور
    def updatePassword(self, e):
        values, textBoxState = self.checkTextBoxData()  # التحقق من صحة البيانات
        if textBoxState:
            self.loaderUi()  # عرض واجهة التحميل
            state, result = self.page.run_task(
                self.sendPatchRequest, "updateUser", values
            ).result()
            if state:
                self.updateUserData(result)  # تحديث بيانات المستخدم
                self.showMessage("تم تحديث كلمة المرور بنجاح")  # عرض رسالة نجاح
                self.did_mount()  # إعادة بناء الواجهة
            else:
                self.did_mount()  # إعادة بناء الواجهة
                self.showMessage(result["password"])  # عرض رسالة الخطأ


class Profile(View):
    # دالة البناء (Constructor)
    # تهيئة الكلاس وتعيين المتغيرات الأولية
    def __init__(self, route, page):
        super().__init__(route=route)  # استدعاء مُنشئ الفئة الأم (View)
        self.page = page  # تعيين الصفحة الحالية
        self.scroll = ScrollMode.AUTO  # تمكين التمرير التلقائي

        # إنشاء أداة اختيار الملفات
        self.selector = FilePicker(
            on_result=self.ChangeProfileImage
        )  # تعيين حدث اختيار الملف
        self.page.overlay.append(self.selector)  # إضافة الأداة إلى الصفحة

        # إنشاء واجهة BottomSheet لتغيير صورة الملف الشخصي
        self.BottomSheet = BottomSheet(
            content=Container(
                content=Column(
                    tight=True,
                    controls=[
                        TextButton(
                            text="تغيير صورة الملف الشخصي",  # نص الزر
                            icon=icons.ADD_A_PHOTO,  # أيقونة الزر
                            on_click=lambda _: self.selector.pick_files(
                                allow_multiple=False,  # عدم السماح باختيار أكثر من ملف
                                allowed_extensions=[
                                    "jpg",
                                    "jpeg",
                                    "png",
                                ],  # أنواع الملفات المسموحة
                                dialog_title="اختيار صورة ملف شخصي",  # عنوان النافذة
                                file_type=FilePickerFileType.IMAGE,  # نوع الملف
                            ),
                            width=float("inf"),  # جعل الزر يأخذ العرض الكامل
                        ),
                    ],
                ),
                width=float("inf"),  # جعل الحاوية تأخذ العرض الكامل
                padding=20,  # الحشو الداخلي
            ),
        )

        # إنشاء شريط التطبيق (AppBar)
        self.appbar = AppBar(
            leading=IconButton(
                icon=icons.ARROW_BACK,  # أيقونة العودة
                icon_color="#ffffff",  # لون الأيقونة
                on_click=lambda x: self.page.go(
                    "/home"
                ),  # حدث النقر للعودة إلى الصفحة الرئيسية
            ),
            title=Text(
                "حماية الاطفال",  # عنوان شريط التطبيق
                size=20,
                weight=FontWeight.BOLD,
                color="#ffffff",  # لون النص
                font_family="ElMessiri",  # نوع الخط
            ),
            toolbar_height=100,  # ارتفاع شريط التطبيق
        )

    # دالة عرض واجهة التحميل
    # تعرض حلقة تحميل أثناء انتظار اكتمال المهام
    def loaderUi(self):
        self.scroll = None
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

    # دالة يتم تنفيذها عند تحميل الصفحة
    # تقوم ببناء واجهة المستخدم
    def did_mount(self):
        self.controls.clear()  # مسح العناصر الحالية
        loader = self.loaderUi()  # عرض واجهة التحميل
        self.controls.append(loader)
        self.buildUi()  # بناء واجهة المستخدم

    # دالة بناء واجهة المستخدم
    # تقوم ببناء واجهة الملف الشخصي
    def buildUi(self):
        self.scroll = ScrollMode.ALWAYS  # تمكين التمرير
        self.controls.clear()  # مسح العناصر الحالية
        userData = self.page.run_task(
            self.page.client_storage.get_async, "userData"
        ).result()  # الحصول على بيانات المستخدم
        self.controls.append(
            ResponsiveRow(
                controls=[
                    Container(height=10),  # مسافة بين العناصر
                    Column(
                        controls=[
                            Container(
                                content=Image(
                                    src=f"{Profile.baseUrl}{userData['profileImage']}",  # عرض صورة الملف الشخصي
                                    width=250,  # عرض الصورة
                                ),
                                border_radius=border_radius.all(
                                    150
                                ),  # حواف مستديرة للصورة
                                on_click=lambda e: self.page.open(
                                    self.BottomSheet
                                ),  # حدث النقر لفتح BottomSheet
                                width=200,  # عرض الحاوية
                                height=200,  # ارتفاع الحاوية
                                border=border.all(
                                    width=0.5, color="black"
                                ),  # إطار الحاوية
                            ),
                            Container(
                                content=Text(
                                    f"{userData['first_name']} {userData['last_name']}",  # عرض الاسم الكامل
                                    size=20,
                                    weight=FontWeight.BOLD,
                                    color="#666666",  # لون النص
                                    font_family="ElMessiri",  # نوع الخط
                                ),
                            ),
                            Container(height=30),  # مسافة بين العناصر
                            Column(
                                controls=[
                                    ResponsiveRow(
                                        controls=[
                                            Container(
                                                content=ListTile(
                                                    title=Text(
                                                        "البيانات الشخصية",  # نص العنصر
                                                        style=TextStyle(
                                                            size=15,
                                                            weight=FontWeight.BOLD,
                                                            font_family="ElMessiri",  # تنسيق النص
                                                        ),
                                                    ),
                                                    trailing=IconButton(
                                                        icon=icons.PERSON,  # أيقونة العنصر
                                                    ),
                                                ),
                                                bgcolor="#ffffff",  # لون الخلفية
                                                border=border.all(
                                                    0.5, "#110b22"
                                                ),  # إطار الحاوية
                                                border_radius=border_radius.all(
                                                    5
                                                ),  # حواف مستديرة
                                                on_click=lambda x: self.page.go(
                                                    "/PersonalInformation"
                                                ),  # حدث النقر للانتقال إلى تعديل المعلومات الشخصية
                                            ),
                                        ],
                                    ),
                                    ResponsiveRow(
                                        controls=[
                                            Container(
                                                content=ListTile(
                                                    title=Text(
                                                        "الامان وكلمة المرور",  # نص العنصر
                                                        style=TextStyle(
                                                            size=15,
                                                            weight=FontWeight.BOLD,
                                                            font_family="ElMessiri",  # تنسيق النص
                                                        ),
                                                    ),
                                                    trailing=IconButton(
                                                        icon=icons.LOCK,  # أيقونة العنصر
                                                    ),
                                                ),
                                                bgcolor="#ffffff",  # لون الخلفية
                                                border=border.all(
                                                    0.5, "#110b22"
                                                ),  # إطار الحاوية
                                                border_radius=border_radius.all(
                                                    5
                                                ),  # حواف مستديرة
                                                on_click=lambda x: self.page.go(
                                                    "/SecurityPasswords"
                                                ),  # حدث النقر للانتقال إلى تغيير كلمة المرور
                                            ),
                                        ],
                                    ),
                                    ResponsiveRow(
                                        controls=[
                                            Container(
                                                content=ListTile(
                                                    title=Text(
                                                        "تسجيل الخروج",  # نص العنصر
                                                        style=TextStyle(
                                                            size=15,
                                                            weight=FontWeight.BOLD,
                                                            font_family="ElMessiri",  # تنسيق النص
                                                        ),
                                                    ),
                                                    trailing=IconButton(
                                                        icon=icons.LOGOUT,  # أيقونة العنصر
                                                    ),
                                                ),
                                                bgcolor="#ffffff",  # لون الخلفية
                                                border=border.all(
                                                    0.5, "#110b22"
                                                ),  # إطار الحاوية
                                                border_radius=border_radius.all(
                                                    5
                                                ),  # حواف مستديرة
                                                on_click=lambda e: self.logOut(),  # حدث النقر لتسجيل الخروج
                                            ),
                                        ],
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

    # دالة تسجيل الخروج
    # تقوم بمسح التخزين المحلي والانتقال إلى الصفحة الرئيسية
    def logOut(self):
        self.page.client_storage.clear()  # مسح التخزين المحلي
        self.page.go("/")  # الانتقال إلى الصفحة الرئيسية

    # دالة إرسال طلب PUT لتغيير صورة الملف الشخصي
    # تقوم بإرسال الصورة المحددة إلى الخادم
    async def sendPutRequest(self, url, files={}):
        access = await self.page.client_storage.get_async(
            "access"
        )  # الحصول على رمز الوصول
        headers = {
            "Authorization": f"Bearer {access}",
            "Accept": "*/*",
            "Cache-Control": "no-cache",
        }
        try:
            response = requests.put(
                url=f"{Profile.baseUrl}/{url}/", files=files, headers=headers
            )
            json = response.json()  # تحويل الاستجابة إلى JSON
            if response.status_code == 200:
                userData = {
                    "username": json["username"],
                    "gender": json["gender"],
                    "first_name": json["first_name"],
                    "last_name": json["last_name"],
                    "profileImage": json["profileImage"],
                }
                await self.page.client_storage.set_async(
                    "userData", userData
                )  # تحديث بيانات المستخدم
                return [True, json]  # إرجاع النتيجة الناجحة
            else:
                return [False, json]  # إرجاع النتيجة الفاشلة
        except requests.exceptions.Timeout:
            return [
                False,
                "اتصال الانترنت بطئ",
            ]  # إرجاع رسالة خطأ في حالة انتهاء المهلة
        except requests.exceptions.ConnectionError:
            return [
                False,
                "حدث خطأ في الاتصال بالخادم. تحقق من اتصالك بالإنترنت.",
            ]  # إرجاع رسالة خطأ في حالة فشل الاتصال

    # دالة عرض واجهة الخطأ
    # تعرض رسالة خطأ مع زر لإعادة المحاولة
    def ErrorUi(self):
        self.scroll = None
        self.controls.clear()
        self.controls.append(
            Column(
                controls=[
                    Container(
                        content=Text(
                            "حدث خطأ الرجاء اعادة المحاولة",  # نص الخطأ
                            style=TextStyle(
                                size=15,
                                weight=FontWeight.BOLD,
                                font_family="ElMessiri",  # تنسيق النص
                            ),
                        ),
                        alignment=alignment.center,  # محاذاة النص في المنتصف
                        expand=True,  # توسيع الحاوية لملء المساحة المتاحة
                    ),
                    Container(
                        content=TextButton(
                            icon=icons.REPLAY_OUTLINED,  # أيقونة إعادة المحاولة
                            text="اعادة المحاولة",  # نص الزر
                            style=ButtonStyle(
                                text_style=TextStyle(
                                    size=15,
                                    weight=FontWeight.BOLD,
                                    font_family="ElMessiri",  # تنسيق النص
                                ),
                            ),
                            on_click=lambda e: self.did_mount(),  # حدث النقر على الزر
                        ),
                        alignment=alignment.center,  # محاذاة الزر في المنتصف
                    ),
                ],
                expand=True,  # توسيع العمود لملء المساحة المتاحة
            )
        )
        self.update()  # تحديث الواجهة

    # دالة عرض واجهة التحميل
    # تعرض حلقة تحميل أثناء انتظار اكتمال المهام
    def loaderUi(self):
        self.scroll = None
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

    # دالة تغيير صورة الملف الشخصي
    # تقوم بمعالجة اختيار الصورة وإرسالها إلى الخادم
    def ChangeProfileImage(self, e):
        self.page.close(self.BottomSheet)  # إغلاق BottomSheet
        if e.files:
            self.controls.clear()  # مسح العناصر الحالية
            loader = self.loaderUi()  # عرض واجهة التحميل
            self.controls.append(loader)
            self.update()  # تحديث الواجهة
            files = {
                "Image": (
                    "image.jpg",
                    open(f"{e.files[0].path}", "rb"),
                    "image/jpeg",
                ),  # تحضير الملف للإرسال
            }
            state, result = self.page.run_task(
                self.sendPutRequest, "uploadProfileImage", files
            ).result()
            if state:
                self.did_mount()  # إعادة بناء الواجهة
            else:
                self.ErrorUi()  # عرض واجهة الخطأ
