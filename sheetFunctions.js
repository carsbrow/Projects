// Helper functions used to categorize data in google sheets
// Implemented into Google Apps Script

// Sums all the positive integers in the column, used for total month income
function sumPositiveFloats() {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    var range = sheet.getRange("B7:B" + sheet.getLastRow());
    var values = range.getValues();
    var sum = 0;
  
    values.forEach(function(row) {
      row.forEach(function(value) {
        if (typeof value === 'number' && value > 0) {
          sum += value;
        }
      });
    });
  
    return sum;
  }
  
  // Sums all the negative integers in the column, used for total month expenses
  function sumNegativeFloats() {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    var range = sheet.getRange("B7:B" + sheet.getLastRow());
    var values = range.getValues();
    var sum = 0;
  
    values.forEach(function(row) {
      row.forEach(function(value) {
        if (typeof value === 'number' && value < 0) {
          sum += value;
        }
      });
    });
  
    return Math.abs(sum);
  }

  // Sums all the transactions in a category, used to egt a spending summary
  function sumTransactionsByCategory(transactionRange, categoryRange, category) {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    var transactions = sheet.getRange(transactionRange).getValues();
    var categories = sheet.getRange(categoryRange).getValues();
    
    var sum = 0;
    
    for (var i = 0; i < transactions.length; i++) {
      var currentCategory = categories[i][0]; 
      
      if (currentCategory === category) {
        var transactionValue = parseFloat(transactions[i][0]);
        
        if (!isNaN(transactionValue)) {
          sum += transactionValue;
        }
      }
    }
    
    return sum;
  }



  