from time import sleep 
from selenium.webdriver.common.by import By

import pandas as pd 
import requests
import seleniumrequests


def process_ceps(file_path: str) -> tuple[pd.DataFrame, list]:
    df = pd.read_csv(file_path)
    df['CEP'] = df['CEP'].str.replace('-', '')

    url = 'https://www.sefanet.pr.gov.br/SefanetV2/Modulos/CIF911.asp?eTpCEP=Est'
    driver = seleniumrequests.Chrome()
    driver.get(url)

    results = pd.DataFrame(columns=['CEP', 'logradouro', 'complemento', 'numero', 'bairro', 'cidade'])
    failed_ceps = []

    for index, row in df.iterrows():
        cep = row['CEP']
        try:
            driver.find_element(By.XPATH, '/html/body/form/table[2]/tbody/tr[2]/td[2]/input').send_keys(cep)
            driver.find_element(By.XPATH, '/html/body/form/table[2]/tbody/tr[4]/td/input[2]').click()
            
            sleep(.5)
            road = driver.find_element(By.XPATH, '/html/body/table[2]/tbody/tr[2]/td[2]').text
            complement = driver.find_element(By.XPATH, '/html/body/table[2]/tbody/tr[3]/td[4]').text
            number = driver.find_element(By.XPATH, '/html/body/table[2]/tbody/tr[3]/td[2]').text
            district = driver.find_element(By.XPATH, '/html/body/table[2]/tbody/tr[4]/td[2]').text
            city = driver.find_element(By.XPATH, '/html/body/table[2]/tbody/tr[4]/td[4]').text
            
            data = {
                'CEP': cep,
                'logradouro': road,
                'complemento': complement,
                'numero': number,
                'bairro': district,
                'cidade': city
            }
            
            results = pd.concat([results, pd.DataFrame([data])], ignore_index=True)
            driver.find_element(By.XPATH, '/html/body/table[2]/tbody/tr[6]/td/input[2]').click()
            
        except Exception as e:
            failed_ceps.append(cep)
            driver.find_element(By.XPATH, '/html/body/table[2]/tbody/tr[4]/td/input[2]').click()

    driver.quit()

    for cep in failed_ceps:
        try:
            response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
            viacep_data = response.json()
            if 'erro' not in viacep_data:
                data = {
                    'CEP': cep,
                    'logradouro': viacep_data.get('logradouro'),
                    'complemento': '',
                    'numero': '',
                    'bairro': viacep_data.get('bairro'),
                    'cidade': viacep_data.get('localidade')
                }

                results = pd.concat([results, pd.DataFrame([data])], ignore_index=True)
                failed_ceps.remove(cep)

        except Exception as e:
            pass

    return results, failed_ceps