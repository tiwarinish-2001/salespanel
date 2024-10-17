from pyexpat.errors import messages
from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth import authenticate, login, logout # type: ignore
from django.contrib.auth.models import User# type: ignore
from django.http import HttpResponse# type: ignore  

from django.contrib.auth import authenticate, login# type: ignore
from django.contrib.auth.decorators import user_passes_test, login_required# type: ignore 
from django.shortcuts import redirect, render# type: ignore
from django.http import HttpResponse# type: ignore

from .models import ClientData, UserClientInteraction# type: ignore
import pandas as pd# type: ignore
from datetime import datetime, date# type: ignore

from .models import ClientData, UserSubmits# type: ignore
from django.contrib import messages # type: ignore
from django.db import transaction # type: ignore
import chardet# type: ignore
from django.utils.timezone import now  # Import now for timestamp# type: ignore



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect('admin_dashboard')
            else:
                login(request, user)
                return redirect('sales_dashboard')
        else:
            return HttpResponse('Invalid username or password.')

    return render(request, 'login.html')

# Admin
@user_passes_test(lambda user: user.is_staff)
def admin_dashboard(request):
    users = User.objects.all()
    if request.method == 'POST':
        selected_user = request.POST.get('selected_user')
        new_user = request.POST.get('new_user')

        if selected_user and new_user:
            ClientData.objects.filter(assigned_user=selected_user).update(assigned_user=new_user) # type: ignore

    return render(request, 'admin_dashboard.html', {'users': users})



@user_passes_test(lambda user: user.is_superuser)
def upload_file(request):
    if request.method == 'POST' and 'csv_file' in request.FILES:
        csv_file = request.FILES['csv_file']
        selected_users = request.POST.getlist('selected_users')

        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(csv_file)

        # Convert 'Investigate_Date' and 'Schedule_Date' to the correct format
        df['Investigate_Date'] = pd.to_datetime(df['Investigate_Date'], format='%d-%m-%Y', errors='coerce')
        df['Schedule_Date'] = pd.to_datetime(df['Schedule_Date'], format='%d-%m-%Y', errors='coerce')

        # First, drop duplicates based on 'Name', 'Email', and 'Lead' where all other fields are the same
        df_unique = df.drop_duplicates(subset=['Name', 'Email', 'Lead', 'Investigate_Date', 'phonenumber', 'Description', 'company_name', 'location'], keep='first')

        # Next, identify groups where 'Name', 'Email', and 'Lead' are the same but other fields differ
        df_diff = df.groupby(['Name', 'Email', 'Lead']).filter(
            lambda x: len(x) > 1 and (
                x['Investigate_Date'].nunique() > 1 or
                x['phonenumber'].nunique() > 1 or
                x['Description'].nunique() > 1 or
                x['company_name'].nunique() > 1 or
                x['location'].nunique() > 1 
            )
        )

        # Combine the unique and different groups
        df_final = pd.concat([df_unique, df_diff]).drop_duplicates()

        # Add Timestamp column
        df_final['Timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Remove existing data from the database based on the 'Name', 'Email', and 'Lead'
        for _, row in df_final.iterrows():
            ClientData.objects.filter(
                name=row['Name'],
                email=row['Email'],
                lead=row['Lead']
            ).delete()  # Delete the previous entries matching 'Name', 'Email', and 'Lead'

        # Split the data based on the number of records specified for each user
        start_idx = 0
        for user in selected_users:
            num_records = int(request.POST.get(f'split_number_{user}', 0))
            
            if num_records > 0:
                # Get chunk of data for this user
                end_idx = start_idx + num_records if start_idx + num_records < len(df_final) else len(df_final)
                user_data = df_final.iloc[start_idx:end_idx]

                # Assign the user to each row in the chunk
                assigned_user = User.objects.get(username=user)
                for _, row in user_data.iterrows():
                    ClientData.objects.create(
                        name=row['Name'],
                        email=row['Email'],
                        phonenumber=row['phonenumber'],
                        company_name=row.get('company_name', ''),  # Add company_name
                        location=row.get('location', ''),  # Add location
                        investigate_date=row['Investigate_Date'].date() if pd.notnull(row['Investigate_Date']) else None,
                        schedule_date=row['Schedule_Date'].date() if pd.notnull(row['Schedule_Date']) else None,
                        lead=row['Lead'],
                        response=row['Response'],
                        assigned_user=assigned_user,
                        description=row.get('Description', ''),  # Add the description column
                    )
                start_idx = end_idx

        # Add a success message for each user
        messages.success(request, "Data has been successfully allocated to the users.")
        return redirect('upload_file')

    users = User.objects.all()
    return render(request, 'upload_file.html', {'users': users})


# Admin
@user_passes_test(lambda user: user.is_staff)
def work_history(request):
    data = UserSubmits.objects.filter(reviewed=1)
      
    return render(request, 'work_history.html', {"data": data})


# Admin
@user_passes_test(lambda user: user.is_staff)
def change_user(request):
    return render(request, 'change_user.html')


@user_passes_test(lambda user: user.is_staff)
def review_work(request):
    # Fetch only the records that are not reviewed
    data = UserSubmits.objects.filter(reviewed=0)
    
    if request.method == "POST":
        for key, value in request.POST.items():
            if key.startswith("delete_"):  # Identify the delete button
                index = key.split('_')[1]
                # Delete the corresponding row from the database
                try:
                    UserSubmits.objects.filter(id=index).delete()
                    print(f"Deleted UserSubmits with id={index}")
                except UserSubmits.DoesNotExist:
                    print(f"UserSubmits with id={index} does not exist")

            elif key.startswith("name_"):  # This identifies each row of data for updates
                index = key.split('_')[1]
                done = request.POST.get(f'done_{index}')

                # Only process the rows that are marked as done (checked)
                if done:
                    # Fetch values from the form
                    name = request.POST.get(f'name_{index}')
                    email = request.POST.get(f'email_{index}')
                    phonenumber = request.POST.get(f'phonenumber_{index}')
                    investigate_date = request.POST.get(f'investigate_date_{index}')
                    schedule_date = request.POST.get(f'schedule_date_{index}')
                    lead = request.POST.get(f'lead_{index}')
                    response = request.POST.get(f'response_{index}')
                    description = request.POST.get(f'description_{index}')  # Get the description field
                    company_name = request.POST.get(f'company_name_{index}')  # Get the company name field
                    location = request.POST.get(f'location_{index}')  # Get the location field
                    assigned_user = request.POST.get(f'assigned_user_{index}')
                    print('assigned_user', assigned_user)

                    # Delete all previous records with the same phonenumber
                    UserSubmits.objects.filter(phonenumber=phonenumber).delete()

                    # Create a new record with the updated data
                    new_submission = UserSubmits(
                        name=name,
                        email=email,
                        phonenumber=phonenumber,
                        company_name=company_name,  # Add company name field
                        location=location,  # Add location field
                        investigate_date=investigate_date,
                        schedule_date=schedule_date,
                        lead=lead,
                        response=response,
                        description=description,
                        assigned_user=assigned_user,
                        reviewed=1  # Mark the data as reviewed
                    )
                    new_submission.save()  # Save the new entry

                    print(f"Replaced old records and saved new UserSubmits for phonenumber={phonenumber}")

        # Redirect after processing to refresh the page with updated data
        return redirect('review_work')
    
    return render(request, 'review_work.html', {"data": data})





# Sales
@login_required
def sales_dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'sales_dashboard.html', {'username': request.user.username, "dashboard_name": "Sales Dashboard"})
    return redirect('login')

# Sales




@login_required
def assigned_data(request):
    user = request.user.username
    submitted_phone_numbers = UserSubmits.objects.filter(assigned_user=user).values_list('phonenumber', flat=True)
    print(submitted_phone_numbers)
    data = ClientData.objects.filter(assigned_user=user).exclude(phonenumber__in=submitted_phone_numbers)
    
    if request.method == "POST":
        # Get data from the form and save it to UserSubmits and UserClientInteraction tables
        for key, value in request.POST.items():
            if key.startswith("name_"):  # this identifies each row of data
                index = key.split('_')[1]
                done = request.POST.get(f'done_{index}')

                # Only process the rows that are marked as done (checked)
                if done:
                    name = request.POST.get(f'name_{index}')
                    email = request.POST.get(f'email_{index}')
                    phonenumber = request.POST.get(f'phonenumber_{index}')
                    investigate_date = request.POST.get(f'investigate_date_{index}')
                    schedule_date = request.POST.get(f'schedule_date_{index}')
                    lead = request.POST.get(f'lead_{index}')
                    response = request.POST.get(f'response_{index}')
                    description = request.POST.get(f'description_{index}')  # Get the description field
                    company_name = request.POST.get(f'company_name_{index}')  # Get the company name field
                    location = request.POST.get(f'location_{index}')  # Get the location field

                    # Save to UserSubmits model
                    UserSubmits.objects.create(
                        name=name,
                        email=email,
                        phonenumber=phonenumber,
                        company_name=company_name,  # Add company name field
                        location=location,  # Add location field
                        investigate_date=investigate_date,
                        schedule_date=schedule_date,
                        lead=lead,
                        response=response,
                        description=description,
                        assigned_user=request.user.username
                    )

                    # Save to UserClientInteraction model
                    UserClientInteraction.objects.create(
                        name=name,
                        email=email,
                        phonenumber=phonenumber,
                        company_name=company_name,  # Add company name field
                        location=location,  # Add location field
                        investigate_date=investigate_date,
                        schedule_date=schedule_date,
                        lead=lead,
                        response=response,
                        description=description,  # Save the description field
                        assigned_user=request.user.username
                    )

        return redirect('assigned_data')

    return render(request, 'assigned_data.html', {"data": data})




@login_required
def user_client_interaction(request):
    user = request.user.username
    interactions = UserClientInteraction.objects.filter(assigned_user=user)
    return render(request, 'user_client_interaction.html', {'interactions': interactions})

# Sales
@login_required
def scheduled_calls(request):
    user = request.user.username
    today_date = date.today()
    print(today_date, user) 
    data = UserSubmits.objects.filter(assigned_user=user, schedule_date=today_date)
# .exclude(investigate_date=today_date)
    print(data)
    return render(request, 'scheduled_calls.html', {"data": data})











