from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

class MySeleniumTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = Options()
        cls.selenium = WebDriver(options=opts)
        cls.selenium.implicitly_wait(5)
        
        # Superuser
        user = User.objects.create_user("isard", "isard@isardvdi.com", "pirineus")
        user.is_superuser = True
        user.is_staff = True
        user.save()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_verificar_permisos_staff(self):
        # 1. Entrem a admin panel
        self.selenium.get(self.live_server_url + '/admin/')
        
        # 2. Localitzar el camp usuari i posem "isard"
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys("isard")
        
        # 3. Localitzar el camp de contrasenya i escribim "pirineus"
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys("pirineus")
        
        # 4. Botó aceptar
        login_button = self.selenium.find_element(By.XPATH, '//input[@type="submit"]')
        login_button.click()
        
        # (entrem...)
        time.sleep(3)

	# 5. Localitzar el link per afegir usuari
        add_user_button = self.selenium.find_element(By.XPATH, '//a[@href="/admin/auth/user/add/"]')
        add_user_button.click()
        
        # (canvi de plana...)
        time.sleep(2)

	# 6. Uusuari pass i pass2
        self.selenium.find_element(By.ID, "id_username").send_keys("staffuser")
        self.selenium.find_element(By.ID, "id_password1").send_keys("15Testing$15")
        self.selenium.find_element(By.ID, "id_password2").send_keys("15Testing$15")
        
        # 7. Clic en guardar
        self.selenium.find_element(By.NAME, "_save").click()
        time.sleep(2)
        
        # 8. Marcar el checkbox d'Staff i guardem
        self.selenium.find_element(By.ID, "id_is_staff").click()
        self.selenium.find_element(By.NAME, "_save").click()
        time.sleep(2)
        
        # 9. Logout per entrar amb el nou usuari
        self.selenium.find_element(By.XPATH, '//form[@id="logout-form"]//button').click()
        time.sleep(2)

        # 10. Login amb el nou usuari
        self.selenium.get(self.live_server_url + '/admin/')
        self.selenium.find_element(By.NAME, "username").send_keys("staffuser")
        self.selenium.find_element(By.NAME, "password").send_keys("15Testing$15")
        self.selenium.find_element(By.XPATH, '//input[@type="submit"]').click()
        time.sleep(2)
        
        # 11. COMPROBACIÓ FINAL - part personalitzada (Mirem si el nou usuari veu les seccions questions i Choices)
        try:
            self.selenium.find_element(By.XPATH, '//a[@href="/admin/polls/question/"]')
            self.fail("L'usuari staff pout veure Questions")
        except NoSuchElementException:
            pass # No la troba, el que suposem que ha de passar.

        try:
            self.selenium.find_element(By.XPATH, '//a[@href="/admin/polls/choice/"]')
            self.fail("L'usuari staff pot veure Choices")
        except NoSuchElementException:
            pass # No la troba
