from main import handler

# Netlify functions expects a handler variable
# Since we already defined 'handler = Mangum(app)' in main.py, 
# we can just re-export it here.
