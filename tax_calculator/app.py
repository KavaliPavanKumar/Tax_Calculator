from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory storage (use a database for production)
user_data = {"username": "user", "password": "password"}
tax_data = {}

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == user_data["username"] and password == user_data["password"]:
            return redirect(url_for("home"))
        else:
            return "Invalid credentials. Try again!"
    return render_template("login.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/input", methods=["GET", "POST"])
def input_data():
    if request.method == "POST":
        tax_data.update(request.form.to_dict())
        tax_data["hra_exemption"] = calculate_hra(
            float(tax_data["basic_salary"]), tax_data["city_type"]
        )
        tax_data["taxable_income"] = calculate_taxable_income(tax_data)
        return redirect(url_for("report"))
    return render_template("input.html")

@app.route("/report")
def report():
    return render_template("report.html", tax_data=tax_data)

def calculate_hra(basic_salary, city_type):
    return 0.5 * basic_salary if city_type.lower() == "metro" else 0.4 * basic_salary

def calculate_taxable_income(data):
    basic_salary = float(data["basic_salary"])
    gross_salary = float(data["gross_salary"])
    exemptions = (
        float(data["pf"]) + float(data["life_insurance"]) + float(data["health_insurance"])
    )
    hra = float(data["hra_exemption"])
    return gross_salary - exemptions - hra

if __name__ == "__main__":
    app.run(debug=True)
