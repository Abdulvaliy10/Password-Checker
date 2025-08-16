import re

def check_password_strength(password):
    strength = 0
    remarks = ""

    # 1. Uzunlik sharti
    if len(password) >= 8:
        strength += 1
    else:
        remarks += "Parol kamida 8 ta belgidan iborat bo‘lishi kerak.\n"

    # 2. Katta harf
    if re.search(r"[A-Z]", password):
        strength += 1
    else:
        remarks += "Katta harf qo‘shing.\n"

    # 3. Kichik harf
    if re.search(r"[a-z]", password):
        strength += 1
    else:
        remarks += "Kichik harf qo‘shing.\n"

    # 4. Raqam
    if re.search(r"[0-9]", password):
        strength += 1
    else:
        remarks += "Raqam qo‘shing.\n"

    # 5. Maxsus belgilar
    if re.search(r"[@$!%*?&]", password):
        strength += 1
    else:
        remarks += "Maxsus belgi qo‘shing (@, $, !, %, *, ?, & ...).\n"

    # Natija chiqarish
    if strength == 5:
        return "Strong ✅"
    elif strength >= 3:
        return "Medium ⚠️\n" + remarks
    else:
        return "Weak ❌\n" + remarks


# Foydalanuvchi parol kiritadi
password = input("Parolni kiriting: ")
print(check_password_strength(password))
