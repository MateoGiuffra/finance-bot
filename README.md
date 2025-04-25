### README: Telegram Bot for Invoice Processing and Financial Tracking

---

#### **Overview**

Welcome to the **Telegram Bot for Invoice Processing and Financial Tracking**! This bot is designed to simplify your financial management by automating the extraction of invoice totals from images and seamlessly updating your Google Sheets with the extracted data. Whether you're managing personal expenses or tracking business finances, this bot is your ultimate assistant.

With a focus on simplicity and efficiency, the bot leverages **Optical Character Recognition (OCR)** technology to extract invoice totals from uploaded images and integrates with **Google Sheets** to organize and track your financial data. It’s perfect for anyone looking to streamline their expense tracking process!

---

#### **Key Features**

- **Invoice Total Extraction**:  
  Upload an image of your invoice, and the bot will use OCR to extract the total amount automatically.

- **Google Sheets Integration**:  
  The bot updates your Google Sheets with the extracted data, organizing it by date and category. It ensures your financial records are always up-to-date and neatly formatted.

- **Dynamic Spreadsheet Management**:  
  Automatically creates new sheets for each month and sorts data in descending order by date.

- **Customizable Categories**:  
  Define your own categories (e.g., Groceries, Utilities, Entertainment) to classify expenses effectively.

- **Error Handling**:  
  Built-in error handling ensures smooth operation even if the OCR fails to detect the total or other unexpected issues arise.

---

#### **How It Works**

1. **Start the Bot**:  
   Use the `/start` command to initialize the bot. You'll be prompted to provide your name and define your expense categories.

2. **Send an Invoice**:  
   Use the `/send` command to send an invoice. First, specify the category for the expense, then upload the image of the invoice. The bot will extract the total and update your Google Sheet.

3. **View Your Data**:  
   Use the `/getsheet` command to get the link to your Google Sheet and view your organized financial data.

4. **Future Enhancements**:  
   Commands like `/totalcategory` and `/total` will allow you to calculate and view totals for specific categories or all expenses for the current month.

---

#### **Technical Details**

The bot is built using the following technologies:

- **Python Libraries**:
  - `pytesseract`: For extracting text from images using OCR.
  - `Pillow (PIL)`: For image processing.
  - `python-telegram-bot`: For building the Telegram bot interface.
  - `gspread` and `gspread_formatting`: For interacting with and formatting Google Sheets.
  - `dotenv`: For managing environment variables securely.

- **Regex Pattern Matching**:  
  The bot uses regular expressions to identify and extract the total amount from the OCR output.

- **Google Sheets API**:  
  The bot dynamically interacts with Google Sheets to create, update, and format spreadsheets.

---

#### **Setup Instructions**

1. **Install Dependencies**:  
   Ensure you have Python installed, then install the required libraries:
   ```bash
   pip install pytesseract pillow python-telegram-bot gspread gspread-formatting python-dotenv
   ```

2. **Set Up Tesseract OCR**:  
   Download and install Tesseract OCR from [here](https://github.com/tesseract-ocr/tesseract). Update the `TESSERACT_CMD` variable in your `.env` file with the path to the Tesseract executable.

3. **Google Sheets API Credentials**:  
   - Create a project in the [Google Cloud Console](https://console.cloud.google.com/).
   - Enable the Google Sheets API and download the credentials JSON file.
   - Share your Google Sheet with the service account email provided in the credentials.

4. **Environment Variables**:  
   Add the following variables to your `.env` file:
   ```env
   TELEGRAM_TOKEN=your_telegram_bot_token
   TESSERACT_CMD=path_to_tesseract_executable
   GOOGLE_CREDENTIALS=path_to_your_credentials_json
   ```

5. **Run the Bot**:  
   Deploy the bot on your server or local machine and start interacting with it via Telegram:
   ```bash
   python bot.py
   ```

---

#### **Commands**

- `/start`: Initialize the bot and set up your name and expense categories.
- `/send`: Send an invoice by specifying a category and uploading an image.
- `/getsheet`: Get the link to your Google Sheet.
- `/help`: View a list of available commands.
- `/totalcategory`: (Coming soon) Get the total for a specific category.
- `/total`: (Coming soon) Get the total for all categories in the current month.

---

#### **Sample Video**

Below is a video demonstrating the bot in action. Watch how it processes an invoice image, extracts the total, and updates the Google Sheet seamlessly.

[INSERT VIDEO LINK HERE]

---

#### **Code Highlights**

1. **Conversation Flow**:  
   The bot uses `ConversationHandler` to guide users through multi-step interactions, such as setting up categories or sending invoices.

2. **Image Processing**:  
   The `set_ticket_total` function extracts the total amount from the uploaded image using OCR and validates the result.

3. **Google Sheets Integration**:  
   The `FinanceSheetManager` class handles all interactions with Google Sheets, including creating new sheets, adding rows, and formatting cells.

4. **Error Handling**:  
   The bot includes robust error handling to manage issues like invalid images, missing totals, or API errors.

---

#### **Future Enhancements**

- **Total Calculation**:  
  Add functionality to calculate and display the total expenses for each category (`/totalcategory`) and all categories (`/total`).

- **Multi-Language Support**:  
  Extend OCR capabilities to support invoices in multiple languages.

- **Advanced Analytics**:  
  Integrate charts and graphs for better visualization of financial data.

- **User Authentication**:  
  Implement user-specific sheets for multi-user environments.

---

#### **Contributing**

If you'd like to contribute to this project, feel free to fork the repository and submit pull requests. Any suggestions or bug reports are welcome!

---

#### **License**

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

#### **Contact**

For any questions or feedback, feel free to reach out to me at [matteogiuffrah40@gmail.com].

---

Thank you for checking out this project! I hope this bot helps you manage your finances more efficiently. 😊