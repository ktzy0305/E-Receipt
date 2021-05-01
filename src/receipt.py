from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT
from datetime import datetime
import io

def generate_receipt(receipt_data):
    # Change timestamp to datetime object
    if "timestamp" in receipt_data.keys():
        time_stamp = receipt_data["timestamp"]
        if isinstance(time_stamp, str):
            receipt_data["timestamp"] = datetime.strptime(time_stamp, "%d/%m/%Y %H:%M:%S")

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

    # justify_style = styles["Justify"]
    # justify_style.fontSize = 11
    justify_style = ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontSize=14)
    align_right_style = ParagraphStyle(name='AlignRight', alignment=TA_RIGHT, fontSize=14)

    # content of the receipt
    receipt_content = []

    # Data To Be Displayed (Top To Bottom)
    retailer = Paragraph(receipt_data["retailer"], normal_center_align)
    address =  Paragraph(receipt_data["address"], normal_center_align)
    gst_reg_no = Paragraph("GST Reg No: " + receipt_data["gst_reg_no"], normal_center_align)

    # Divider
    divider = Paragraph("-"*94, justify_style)

    # Meta Information
    cashier_id =  Paragraph("Cashier: {}".format(receipt_data["cashier_id"]), justify_style)
    transaction_id = Paragraph("Transaction No: {}".format(receipt_data["transaction_id"]), justify_style)
    transaction_date = Paragraph("Date: {}".format(receipt_data["timestamp"].strftime("%d/%m/%Y")), justify_style)
    transaction_time = Paragraph("Time: {}".format(receipt_data["timestamp"].strftime("%H:%M")), justify_style)


    receipt_content.append(retailer)
    receipt_content.append(address)
    receipt_content.append(gst_reg_no)
    receipt_content.append(divider)
    receipt_content.append(cashier_id)
    receipt_content.append(transaction_id)
    receipt_content.append(transaction_date)
    receipt_content.append(transaction_time)
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
    gst = Paragraph("GST (7%): {:.2f}".format(receipt_data["gst"]), align_right_style)
    total = Paragraph("Total: {:.2f}".format(receipt_data["total"]), align_right_style)

    receipt_content.append(subtotal)
    receipt_content.append(gst)
    receipt_content.append(total)
    receipt_content.append(divider)

    # Payment
    payment = Paragraph("{}: {:.2f}".format(receipt_data["paymentMethod"].capitalize(), receipt_data["received"]), align_right_style)
    receipt_content.append(payment)

    if "change" in receipt_data.keys():
        change = Paragraph("Change: {:.2f}".format(receipt_data["change"]), align_right_style)
        receipt_content.append(change)

    refund_policy = Paragraph("<br/><br/>{}".format(receipt_data["refund_policy"]), normal_center_align)
    receipt_content.append(refund_policy)

    pdf.build(receipt_content)

    target_stream.seek(0)
    return target_stream