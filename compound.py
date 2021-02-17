def compound(principal, annual_rate, years, compounds_per_year):

    compound = principal * (1 + (annual_rate / 100) / compounds_per_year)**(years * compounds_per_year)
    interest = round(compound - principal, 2)
    return interest



