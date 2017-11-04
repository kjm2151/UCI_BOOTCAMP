Sub StockSolution()

Dim total As Double
Dim i As Long
Dim change As Single
Dim j As Integer
Dim start As Long
Dim rowCount As Long
Dim percentChange As Single
Dim days As Integer
Dim dailyChange As Single
Dim averageChange As Single

' Set initial values
j = 0
total = 0
change = 0
start = 2
dailyChange = 0


Worksheets("Result").Range("A1").Value = "Ticker"
Worksheets("Result").Range("B1").Value = "Total Change"
Worksheets("Result").Range("C1").Value = "% of Change"
Worksheets("Result").Range("D1").Value = "Avg. Daily Change"
Worksheets("Result").Range("E1").Value = "Total vol."


' get the row number of the last row with data
rowCount = Cells(Rows.Count, "A").End(xlUp).Row

For i = 2 To rowCount

' If ticker changes then print results
    If Cells(i + 1, 1).Value <> Cells(i, 1).Value Then

        ' Stores results in variables
        total = total + Cells(i, 7).Value
        change = (Cells(i, 6) - Cells(start, 3))
        percentChange = Round((change / Cells(start, 3) * 100), 2)
        dailyChange = dailyChange + (Cells(i, 4) - Cells(i, 5))

        ' Average change
        days = (i - start) + 1
        averageChange = dailyChange / days

        ' start of the next stock ticker
        start = i + 1

        ' print the results to a seperate worksheet
        Worksheets("Result").Range("A" & 2 + j).Value = Cells(i, 1).Value
        Worksheets("Result").Range("B" & 2 + j).Value = Round(change, 2)
        Worksheets("Result").Range("C" & 2 + j).Value = "%" & percentChange
        Worksheets("Result").Range("D" & 2 + j).Value = averageChange
        Worksheets("Result").Range("E" & 2 + j).Value = total

       ' colors positives green and negatives red
        Select Case change
            Case Is > 0
                Worksheets("Result").Range("B" & 2 + j).Interior.ColorIndex = 4
            Case Is < 0
                Worksheets("Result").Range("B" & 2 + j).Interior.ColorIndex = 3
            Case Else
                Worksheets("Result").Range("B" & 2 + j).Interior.ColorIndex = 0
        End Select



        ' reset variables for new stock ticker
        total = 0
        change = 0
        j = j + 1
        days = 0
        dailyChange = 0

   ' If ticker is still the same add results
    Else
        total = total + Worksheets("Result").Cells(i, 7).Value
        change = change + (Worksheets("Result").Cells(i, 6) - Worksheets("Result").Cells(i, 3))

        ' change in high and low
        dailyChange = dailyChange + (Worksheets("Result").Cells(i, 4) - Worksheets("Result").Cells(i, 5))


    End If

Next i

Dim max_vol As Integer
Dim max_inc As Single
Dim max_dec As Single
Dim max_change As Single

Worksheets("Result").Range("G2").Value = "Total shares"
Worksheets("Result").Range("G5").Value = "Greatest % Increase"
Worksheets("Result").Range("G8").Value = "Greatest % Decr"
Worksheets("Result").Range("G10").Value = "Greatest Daily Avg. Daily change"
Worksheets("Result").Range("I1").Value = "Ticker"



'Find maximum value of the row

max_vol = WorksheetFunction.Max(Range("E:E"))
max_inc = WorksheetFunction.Max(Range("C:C"))
max_dec = WorksheetFunction.Max(Range("C:C"))
max_change = WorksheetFunction.Max(Range("A:A"))


Worksheets("Result").Range("H2").Value = max_vol
Worksheets("Result").Range("H5").Value = max_inc
Worksheets("Result").Range("H8").Value = max_dec
Worksheets("Result").Range("H10").Value = max_change


'Find matching Ticket value

For i = 1 To rowCount
    If Cells(i, 5).Value = max_vol Then
        Range("I2").Value = Cells(i, 1).Value
    End If
    
    i = 0
    
    If Cells(i, 3).Value = max_inc Then
        Range("I5").Value = Cells(i, 1).Value
    End If
    
    i = 0
    
    If Cells(i, 3).Value = max_dec Then
        Range("I8").Value = Cells(i, 1).Value
    End If
    
    
    If Cells(i, 4).Value = max_change Then
        Range("I10").Value = Cells(i, 1).Value
    End If

Next i


End Sub