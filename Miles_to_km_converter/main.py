import tkinter

def calculate():
    miles = float(miles_entry.get()) * 1.609344
    miles = '{:.3f}'.format(miles)  # точность до 3 знаков
    label_miles_calculated.config(text=miles)

window = tkinter.Tk()
window.title('Mile to Km Converter')
window.minsize(width=200, height=100)
window.config(padx=10, pady=10)

# entry
miles_entry = tkinter.Entry(width=5)
miles_entry.grid(column=1, row=0)

# label_'miles'
label_miles = tkinter.Label(text='Miles')
label_miles.grid(column=2, row=0)

# label_isequal
label_isequal = tkinter.Label(text='is equal to')
label_isequal.grid(column=0, row=1)

miles = 0
# label_miles.calculated
label_miles_calculated = tkinter.Label(text=miles)
label_miles_calculated.grid(column=1, row=1)

# label 'km'
label_km = tkinter.Label(text='Km')
label_km.grid(column=2, row=1)

# button calculate
button_calculate = tkinter.Button(text='Calculate', command=calculate)
button_calculate.grid(column=1, row=2)


window.mainloop()