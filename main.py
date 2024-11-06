from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    username = "wassim.backer@copart.com"
    password = "bacSummer@2024"

    options = webdriver.EdgeOptions()
    options.add_argument("inprivate")
    options.add_argument("--disable-identity")
    
    driver = webdriver.Edge(options=options)

    url = "https://copart.okta.com/oauth2/v1/authorize?client_id=0oa1smkb78Y9lc6GI357&response_type=code&scope=offline_access&redirect_uri=https://g2.copart.co.uk/login&state=okta"
    driver.get(url)

    try:
        username_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "identifier"))
        )
        username_field.send_keys(username)

        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='o-form-button-bar']//input[@type='submit']"))
        )
        submit_button.click()

        password_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "credentials.passcode"))
        )
        password_field.send_keys(password)

        verify_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@class='button button-primary' and @type='submit']"))
        )
        verify_button.click()

        time.sleep(5)

        otp_api_url = "https://bumblebeex.prodt.co/api:Yf2mChG1/otp"
        headers = {
            "x-data-source": "staging",
            "x-branch": "v1"
        }
        
        otp_response = requests.get(otp_api_url, headers=headers, timeout=20)

        if otp_response.status_code == 200:
            otp = otp_response.text

            totp_field = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.NAME, "credentials.totp"))
            )
            totp_field.send_keys(otp)

            totp_verify_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@class='button button-primary' and @type='submit']"))
            )
            totp_verify_button.click()

            return jsonify({"message": "Logged in successfully!", "otp": otp}), 200
        else:
            return jsonify({"error": f"Failed to retrieve OTP. Status code: {otp_response.status_code}"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        time.sleep(5)
        driver.quit()

if __name__ == '__main__':
    app.run(debug=True)
