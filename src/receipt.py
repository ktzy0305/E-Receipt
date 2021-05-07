from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT
from datetime import datetime
import io

def generate_receipt(receipt_data):
    # Generate a byte stream for the PDF 
    target_stream = io.BytesIO()

    # creating a Base Document Template of page size A4
    pdf = SimpleDocTemplate( target_stream , pagesize = A4 )

   # standard stylesheet defined within reportlab itself
    styles = getSampleStyleSheet()

    # Styles
    normal_center_align = styles['Normal']
    normal_center_align.alignment = 1
    normal_center_align.fontSize = 12

    justify_style = ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontSize=14)
    align_right_style = ParagraphStyle(name='AlignRight', alignment=TA_RIGHT, fontSize=14)

    # content of the receipt
    receipt_content = []

    # Divider
    divider = Paragraph("-"*94, justify_style)

    # Get keys from receipt_data
    keys = receipt_data.keys()

    # Change timestamp to datetime object
    if "timestamp" in keys:
        time_stamp = receipt_data["timestamp"]
        if isinstance(time_stamp, str):
            receipt_data["timestamp"] = datetime.strptime(time_stamp, "%d/%m/%Y %H:%M:%S")

    # Data To Be Displayed (Top To Bottom)
    retailer = Paragraph(receipt_data["retailer"], normal_center_align)
    address =  Paragraph(receipt_data["address"], normal_center_align)
    
    receipt_content.append(retailer)
    receipt_content.append(address)

    # For businesses that charge Goods & Services Tax (GST) and in countries that require a GST Registration Number
    if "gst_reg_no" in keys:
        gst_reg_no = Paragraph("GST Reg No: " + receipt_data["gst_reg_no"], normal_center_align)
        receipt_content.append(gst_reg_no)

    receipt_content.append(divider)

    # Meta Information
    cashier_id =  Paragraph("Cashier: {}".format(receipt_data["cashier_id"]), justify_style)
    transaction_id = Paragraph("Transaction No: {}".format(receipt_data["transaction_id"]), justify_style)
    transaction_date = Paragraph("Date: {}".format(receipt_data["timestamp"].strftime("%d/%m/%Y")), justify_style)
    transaction_time = Paragraph("Time: {}".format(receipt_data["timestamp"].strftime("%H:%M")), justify_style)

    receipt_content.append(cashier_id)
    receipt_content.append(transaction_id)
    receipt_content.append(transaction_date)
    receipt_content.append(transaction_time)

    # Divider
    receipt_content.append(divider)

    # Products
    for product in receipt_data["products"]:
        receipt_content.append(
            Paragraph(
                "{}{}{}{}{:.2f}<br/><br/>"
                .format(
                    product["qty"], 
                    "&nbsp;" * 8, 
                    product["name"], 
                    "&nbsp;" * ( 100 - (len(product["name"]) + 8 + len(str(product["qty"])) + len(str(product["total"])) )), 
                    product["total"]
                ),
                justify_style
            )
        )
    receipt_content.append(divider)

    # Subtotal
    subtotal = Paragraph("Subtotal: {:.2f}".format(receipt_data["subtotal"]), align_right_style)
    receipt_content.append(subtotal)
    
    # For receipts with GST
    if "gst" in keys:
        gst = Paragraph("GST (7%): {:.2f}".format(receipt_data["gst"]), align_right_style)
        receipt_content.append(gst)
    
    # Total and subtotal might sometimes be different with vouchers, discounts etc...
    total = Paragraph("Total: {:.2f}".format(receipt_data["total"]), align_right_style)
    receipt_content.append(total)
    
    # Divider
    receipt_content.append(divider)

    # Payment
    payment = Paragraph("{}: {:.2f}".format(receipt_data["payment_method"].capitalize(), receipt_data["received"]), align_right_style)
    receipt_content.append(payment)

    # Some payment methods like NETS and Credit Card do not require change.
    if "change" in receipt_data.keys():
        change = Paragraph("Change: {:.2f}".format(receipt_data["change"]), align_right_style)
        receipt_content.append(change)

    if "refund_policy" in keys:
        refund_policy = Paragraph("<br/><br/>{}".format(receipt_data["refund_policy"]), normal_center_align)
        receipt_content.append(refund_policy)

    # Build the PDF
    pdf.build(receipt_content)
    # Reference pointing to the beginning of the file 
    target_stream.seek(0)
    return target_stream