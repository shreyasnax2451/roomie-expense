from PIL import Image
import pytesseract

def parse_expense_to_list(raw_text: str) -> list:
    expense_data = []
    for line in raw_text.split("\n"):
        line = line.strip()
        if not line:
            continue

        if "-" in line:
            item, amount = line.split("-", 1)
            item = item.strip()
            amount = amount.replace(" ", "")
        
            if "+" in amount:
                parts = amount.split("+")
                total = sum(int(p) for p in parts)
            else:
                total = int(amount)
            
            expense_data.append({
                "source_of_expense": item,
                "amount": total
            })

    return expense_data

def parse_expense_from_image(is_image_uploaded) -> list:
    """
    Parse the image and return expense data in list[dict]
    """
    if is_image_uploaded:
        img = Image.open(is_image_uploaded)
        text = pytesseract.image_to_string(img)
        expense_data = parse_expense_to_list(text)
        return expense_data
