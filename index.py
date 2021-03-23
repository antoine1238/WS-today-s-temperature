from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd


# opciones de navegación
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--dissable-extensions")

driver = webdriver.Chrome(executable_path=r'./chromedriver', chrome_options=options)

# -------- Inicialización -----------
driver.get("https://www.eltiempo.es")

# Cierra el cookie
WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
        "button.didomi-components-button.didomi-button.didomi-dismiss-button.didomi-components-button--color.didomi-button-highlight.highlight-button")))\
    .click()

# escribe en la barra de busqueda "madrid"
WebDriverWait(driver, 10)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR,\
        "input#inputSearch")))\
    .send_keys("Madrid")

# Pulsa el icono de buscar 
WebDriverWait(driver, 10)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR,\
        "i.icon.icon-search")))\
    .click()

# presiona el primer resultado  "madrid"
WebDriverWait(driver, 10)\
    .until(EC.element_to_be_clickable((By.XPATH,\
        '//*[@id="page"]/main/div[4]/div/section[2]/section/div/ul/li[1]/a/strong')))\
    .click()

# Presiona el boton "por horas" de el clima de madrid
WebDriverWait(driver, 10)\
    .until(EC.element_to_be_clickable((By.XPATH,\
        '//*[@id="cityTable"]/div/article/section[1]/ul/li[2]/a')))\
    .click()

# Esperar a que se cargue la caja de horarios. Pero no hacer nada
WebDriverWait(driver, 10)\
    .until(EC.element_to_be_clickable((By.XPATH,\
        '/html/body/div[7]/main/div[4]/div/section[4]/section/div[1]')))


#----- Manejo de datos sobre las temperaturas ------
texto_columnas = driver.find_element_by_xpath('/html/body/div[7]/main/div[4]/div/section[4]/section/div[1]')
texto_columnas = texto_columnas.text

tiempo_hoy = texto_columnas.split("Mañana")[0].split("Hoy")[1].split("\n")[1:-1]

horas = []
grados = []
velocidad = []

for i in range(0, len(tiempo_hoy), 4):
    horas.append(tiempo_hoy[i])
    grados.append(tiempo_hoy[i+1])
    velocidad.append(tiempo_hoy[i+2] + "Km")

df = pd.DataFrame({"Horas": horas, "Temperatura": grados, "Velocidad(Km)": velocidad})
df.to_csv("tiempo.csv")
driver.quit()
print(df)

