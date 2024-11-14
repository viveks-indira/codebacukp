import xmlrpc.client

# Connection details
url = 'https://crmindira-crm-19julystaging-14299297.dev.odoo.com/'
db = 'crmindira-crm-19julystaging-14299297'
username = 'sharshit@indiratrade.com'
password = 'Crm@123'

# Establish connection
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})

models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

# Define the mailing campaign details
campaign_name = "Mailing List Campaign with Updated HTML"
subject = "Special Offer for Our Mailing List!"
html_content = """
<html>
    <body>
        <div class="o_layout oe_unremovable oe_unmovable bg-200 o_empty_theme" data-name="Mailing"><style id="design-element"></style><div class="container o_mail_wrapper o_mail_regular oe_unremovable"><div class="row"><div class="col o_mail_no_options o_mail_wrapper_td bg-white oe_structure o_editable theme_selection_done">
  <main style="max-width: 680px; margin: auto; background-color:#eef3ff; padding: 20px; ">
      <div style="max-width: 630px; margin: auto; background-color: #ffffff; border-radius: 15px; padding: 20px;">

          <div style="text-align: center; margin-bottom: 0px;">
              <img src="https://www.indiratrade.com/stock_broker/img/id.png" alt="Company Logo" style="width: 120px; height: auto;" loading="">
          </div>

          <h2 style="color: #333; text-align: center; border-bottom: 1px solid #002e74;margin-top: 3px;"></h2>
          <div style="text-align: center; margin: 20px 0; margin-bottom: 0;">
              <img src="https://iili.io/dsuIbCQ.png" alt="Hyundai Motor India Limited" style="width: 40%;height: auto; margin-top: 10px;" loading="">
          </div>
          <p style="margin-bottom:0px;font-size: 18px;">Hi <t t-out="object.name or '''User'''"></t><strong style="color: #002e74; font-size: 18px;">&nbsp;</strong><img src="https://iili.io/dsuzEfS.md.png" alt="Icon" style="width: 30px; height: 30px; vertical-align: middle;" loading=""></p>
          <p style="font-size: 15.7px; line-height: 1.5;margin-top: 1px;">
              Initial Public Offering (IPO) for
              <strong>Swiggy Limited</strong> has launched today
              <strong style="color: #28a77d;"> (06/11/2024).</strong>.
              <br>
          </p>
          <div style="background-color: #eef3ff; padding: 10px; border-radius: 8px; margin: 10px 0;">
              <h3 style="color: #002e74; margin-top: 8px; margin-bottom: 12px; font-size: 18px; line-height: 25px;">
                  <img src="https://iili.io/dsuxOFt.md.png" alt="Key Details Icon" style="width: 25px; height: 25px; vertical-align: middle; margin-right: 5px;margin-bottom: 5px;" loading="">
                  Key Details:
              </h3>

              <p style="color: #414141;margin-bottom: 0px;margin-top: 5px;font-size: 15.7px;"><strong>IPO
                      Name:</strong> Swiggy Limited </p>
              <p style="color: #414141;margin-top: 7px;font-size: 15.7px;margin-bottom: 0;"><strong>Open
                      Date:</strong>Nov 6, 2024</p>
              <p style="color: #414141;margin-top: 7px;font-size: 15.7px;"><strong>Close
                      Date:</strong> Nov 08, 2024</p>
          </div>

          <h3 style="color: #002e74; margin-top: 25px; margin-bottom: 5px; font-size: 18px; display: flex; align-items: center;">
              <img src="https://iili.io/dsuqNxS.md.png" alt="Icon" style="width: 25px; height: 25px; margin-right: 8px;" loading="">
              Company Overview:
          </h3>
          <p style="color: #000000; line-height: 1.6;margin-top: 5px;font-size: 15.7px; ">Swiggy Limited, is one of India’s leading convenience platforms. They have revolutionized the delivery and hyperlocal commerce space, offering a wide array of services through a single app, including food and grocery delivery, restaurant reservations, event bookings, and more.Swiggy’s business spans five key segments : Food Delivery, Out-of-Home Consumption, Quick Commerce, Supply Chain & Distribution (B2B Logistics), Platform Innovations (including Swiggy Genie and Swiggy Minis). Swiggy has demonstrated impressive growth, with revenue reaching ₹11,247 crore in FY24, up from ₹8,264 crore in FY23, and ₹5,704 crore in FY22. </p>
          <h3 style="color: #002e74; margin-top: 25px; margin-bottom: 5px; font-size: 18px; display: flex; align-items: center;">
            Use of proceeds : 
          </h3>
          <ul style="color: #000000; line-height: 1.6;margin-top: 5px; font-size: 15.7px; padding-left: 0;margin-left: 4px;">
            <li>Repayment of loans</li>
            <li>Dark store expansion under subsidiary<strong> Scootsy</strong></li>
            <li>Investment in technology, cloud storage, and brand marketing</li>
            <li>Corporate growth and strategic initiatives</li>
        </ul>

        <h3 style="color: #002e74; margin-top: 25px; margin-bottom: 5px; font-size: 18px; display: flex; align-items: center;">
            
            Investment Considerations :
        </h3>
        <p style="color: #000000; line-height: 1.6;margin-top: 5px;font-size: 15.7px; ">
            Swiggy’s IPO comes at a time of positive operational improvements, as seen in its upward trajectory in revenue, 
            operating profit margin (OPM), and return on equity (ROE). While the company’s competitor Zomato has shown profitability, 
            Swiggy’s business model and growth potential make it a promising investment opportunity. Despite the challenges of current 
            market conditions,<strong> we recommend considering this IPO with a neutral outlook.</strong>  </p>
       
          <h3 style="color: #002e74; margin-top: 27px; margin-bottom: 5px; font-size: 18px; display: flex; align-items: center;">
              <img src="https://iili.io/dsu3zvV.md.png" alt="Icon" style="width: 25px; height: 25px; margin-right: 8px;" loading="">
              Application Details:
          </h3>

          <ul style="color: #000000; line-height: 1.6;margin-top: 5px; font-size: 15.7px;list-style-type: none; padding-left: 0;margin-left: 0;">
              <li><strong>Retail :</strong> 1 lot, 38 Shares, Rs. 14,280</li>
              <li><strong>S-HNI :</strong> 14 lots, 532 Shares, Rs. 2,07,480</li>
              <li><strong>B-HNI :</strong>68 lots, 2,584 Shares, Rs. 10,07,760</li>
          </ul>

          <table width="100%" style="margin: 10px 0;">
              <tbody><tr>
                  <td style="text-align: center;">
                      <a href="https://ipo.indiratrade.com:83/" style="display: inline-block; font-size: 14px; background-color: #28a77d; color: white; padding: 8px 20px; border-radius: 5px; text-decoration: none; font-weight: bold; transition: all 0.3s ease;">
                          APPLY NOW
                      </a>
                  </td>
              </tr>
          </tbody></table>                

          <p style="color: #000000; display: flex; align-items: center; font-size: 15.7px;">
              To learn more, visit
              <img src="https://iili.io/dsu97Nn.md.png" alt="Icon" style="width: 16px; height: 16px; margin: 2px 4px; vertical-align: middle;" loading="">
              <a href="https://www.indiratrade.com/" style="color: #002e74; text-decoration: none; font-weight: bold;">our
                  website</a>.
          </p>
          
          <p style="color: #000000; font-size: 15.7px; margin-bottom: 7px;">
              If you have any questions or need assistance, feel free to
              reach out to our support team at any of these numbers:-
              <span style="font-weight: bold; color: #333; font-size: 15.7px;">
                  </span></p><div style="display: block;">
                      <a href="tel:+917970007871" style="text-decoration: none; font-weight: 600; color: #002e74;">
                          <img src="https://iili.io/dsuoa7s.md.png" alt="Icon" style="width: 20px; height: 20px; vertical-align: middle; margin-bottom: 2px;" loading="">
                          7970007871
                      </a>
                  </div>
                  <div style="display: block;">
                      <a href="tel:+07314797170" style="text-decoration: none; font-weight: 600; color: #002e74;">
                          <img src="https://iili.io/dsuoa7s.md.png" alt="Icon" style="width: 20px; height: 20px; vertical-align: middle;margin-bottom: 2px;" loading="">
                          7314797170
                      </a>
                  </div>
                  <div style="display: block;">
                      <a href="tel:+07314797171" style="text-decoration: none; font-weight: 600; color: #002e74;">
                          <img src="https://iili.io/dsuoa7s.md.png" alt="Icon" style="width: 20px; height: 20px; vertical-align: middle;margin-bottom: 2px;" loading="">
                          7314797171
                      </a>
                  </div>
              
          <p></p>

          <ul style="list-style-type: none; padding: 0; margin-top: 0; line-height: 1.5; letter-spacing: 0.56px;">
          <li style="font-weight: 600; color: #383838; font-size: 15px; margin-bottom: 10px;margin-top: 18px;padding-left: 0;margin-left: 0;">Download
            our app on your preferred platform:</li>
          <div style="display: flex; align-items: center; gap: 20px;">
            <div style="display: flex; align-items: center;">
              <a href="https://play.google.com/store/apps/details?id=com.wave.indira&amp;hl=en_IN" target="_blank">
                <img src="https://i.imghippo.com/files/Xy0Sq1728991021.png" alt="Android Image" style="width: 100px; height: auto; margin-right: 10px;" loading="">
              </a>
            </div>
            <div style="display: flex; align-items: center;">
              <a href="https://shorturl.at/UOYe1" target="_blank">
                <img src="https://i.imghippo.com/files/xIoH91728991095.png" alt="iOS Image" style="width: 100px; height: auto; margin-right: 10px;" loading="">
              </a>
            </div>
          </div>
        
      </ul>

          <p style="margin: 0; margin-top: 15px; font-size: 15.7px; font-weight: 600; line-height: 1.5; letter-spacing: 0.56px; color: #333;">
              Warm regards,
              <br>
              <span style="font-weight: 600; color: #002e74;font-size: 15.7px;">
                  <img src="https://iili.io/dsunr5G.md.png" alt="Icon" style="width: 24px; height: 24px; vertical-align: middle;" loading="">Team
                  INDIRA</span>
          </p>

          <p style="font-size: 15.7px; color: #000000; font-size: 14px; line-height: 1.5; margin-top: 15px; border-top: 1px solid #eaeaea; padding-top: 10px;">
              Disclaimer: This information is purely for educational
              purposes and doesn’t promote any particular stock or IPO.
              Moreover, we recommend you do your own research before
              investing in any IPO/STOCKS. We are not at all responsible
              for any financial decision taken by you!
          </p>

      </div>
      <footer style="
    width: 100%;
    max-width: 490px;
    margin: 20px auto 0;
    text-align: center;
  ">
          <p style="
      margin: 0;
      margin-top: 20px;
      font-size: 15.7px;
      font-weight: 600;
      color: #434343;
    ">
              Indira Securities Private Limited
          </p>
          <p style="margin: 0; margin-top: 8px; color: #434343; font-weight: 600;font-size: 15.7px;">
              204 Amar Darshan, 28/02, Old
              Palasia, Saket Nagar, Indore,
              Madhya Pradesh 452018
          </p>
          <div style="margin: 0; margin-top: 16px;">
              <a href="https://www.facebook.com/indirasecurities/" target="_blank" style="display: inline-block; margin-left: 8px; text-decoration: none;" onmouseover="this.children[0].style.transform = 'scale(1.1)';" onmouseout="this.children[0].style.transform = 'scale(1)';">
                  <img src="https://iili.io/dsuRwP4.md.png" alt="Facebook" style="width: 25px; height: 25px; transition: transform 0.2s ease-in-out;" loading="">
              </a>
              <a href="https://www.instagram.com/indira_securities/" target="_blank" style="display: inline-block; margin-left: 10px; text-decoration: none;" onmouseover="this.children[0].style.transform = 'scale(1.1)';" onmouseout="this.children[0].style.transform = 'scale(1)';">
                  <img src="https://iili.io/dsuAWEQ.md.png" alt="Instagram" style="width: 25px; height: 25px; transition: transform 0.2s ease-in-out;" loading="">
              </a>
              <a href="https://twitter.com/indiratrade" target="_blank" style="display: inline-block; margin-left: 10px; text-decoration: none;" onmouseover="this.children[0].style.transform = 'scale(1.1)';" onmouseout="this.children[0].style.transform = 'scale(1)';">
                  <img src="https://iili.io/dsuugd7.md.png" alt="Twitter" style="width: 25px; height: 25px; transition: transform 0.2s ease-in-out;" loading="">
              </a>

              <a href="https://api.whatsapp.com/send?phone=+919329099009&amp;text=Hello" target="_blank" style="display: inline-block; margin-left: 10px; text-decoration: none;" onmouseover="this.children[0].style.transform = 'scale(1.1)';" onmouseout="this.children[0].style.transform = 'scale(1)';">
                  <img src="https://iili.io/dsu5jmF.md.png" alt="WhatsApp" style="width: 25px; height: 25px; transition: transform 0.2s ease-in-out;" loading="">
              </a>
              <a href="https://www.youtube.com/channel/UCBLn3-MepTq4-0JObCNb0yA" target="_blank" style="display: inline-block; margin-left: 10px; text-decoration: none;" onmouseover="this.children[0].style.transform = 'scale(1.1)';" onmouseout="this.children[0].style.transform = 'scale(1)';">
                  <img src="https://iili.io/dsuTmDG.md.png" alt="YouTube" style="width: 25px; height: 25px; transition: transform 0.2s ease-in-out;" loading="">
              </a>
          </div>

          <p style="margin: 0; margin-top: 20px; color: #434343; font-weight: 600;font-size: 15.7px;">
              Copyright © 2024 Indira Securities pvt ltd. All rights
              reserved.
          </p>
      </footer>
  </main>

</div></div></div></div>
    </body>
</html>
"""

# Mailing list ID to target specific recipients
mailing_list_id = 25  # Replace this with your actual mailing list ID

# Step 1: Create the campaign with basic information
mailing_id = models.execute_kw(db, uid, password, 'mailing.mailing', 'create', [{
    'name': campaign_name,
    'subject': subject,
    'contact_list_ids': [(6, 0, [mailing_list_id])],  # Link the mailing list
}])

# Step 2: Use the `write` method to explicitly update the `body_html`
models.execute_kw(db, uid, password, 'mailing.mailing', 'write', [[mailing_id], {
    'body_html': html_content,
}])

print(f"Mailing campaign created with ID: {mailing_id} and HTML content updated.")
print("done")

