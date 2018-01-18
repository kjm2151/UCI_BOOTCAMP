# 1a. Display the first and last names of all actors from the table actor.
select first_name, last_name
from sakila.actor;

# 1b. Display the first and last name of each actor in a single column in upper case letters. Name the column Actor Name.
select upper(concat(first_name,' ',last_name)) as "Actor Name"
from sakila.actor;

# 2a. You need to find the ID number, first name, and last name of an actor, of whom you know only the first name, "Joe." What is one query would you use to obtain this information?
select actor_id, first_name, last_name
from sakila.actor
where first_name = 'Joe';

# 2b. Find all actors whose last name contain the letters GEN:
select *
from sakila.actor
where upper(last_name) like '%GEN%';

# 2c. Find all actors whose last names contain the letters LI. This time, order the rows by last name and first name, in that order:
select *
from sakila.actor
where upper(last_name) like '%LI%'
order by last_name, first_name;

# 2d. Using IN, display the country_id and country columns of the following countries: Afghanistan, Bangladesh, and China:
select *
from sakila.country
where country in ('Afghanistan','Bangladesh','China');

# 3a. Add a middle_name column to the table actor. Position it between first_name and last_name. Hint: you will need to specify the data type.
alter table sakila.actor
add column middle_name varchar(45) after first_name;

# 3b. You realize that some of these actors have tremendously long last names. Change the data type of the middle_name column to blobs.
alter table sakila.actor
modify column middle_name blob;

# 3c. Now delete the middle_name column.
alter table sakila.actor
drop column middle_name;

# 4a. List the last names of actors, as well as how many actors have that last name.
select last_name, count(*)
from sakila.actor
group by last_name
order by count(*) desc;

# 4b. List last names of actors and the number of actors who have that last name, but only for names that are shared by at least two actors
select last_name, count(*)
from sakila.actor
group by last_name
having count(*) >= 2
order by count(*) desc;

# 4c. Oh, no! The actor HARPO WILLIAMS was accidentally entered in the actor table as GROUCHO WILLIAMS, the name of Harpo's second cousin's husband's yoga teacher. Write a query to fix the record.
update sakila.actor #actor_id = 172
set first_name = 'HAROP', last_name = 'WILLIAMS'
where first_name = 'GROUCHO'
and last_name = 'WILLIAMS';

select *
from sakila.actor
where actor_id = 172;

/* 4d. Perhaps we were too hasty in changing GROUCHO to HARPO. It turns out that GROUCHO was the correct name after all! In a single query, if the first name of the actor is currently HARPO, 
 change it to GROUCHO. Otherwise, change the first name to MUCHO GROUCHO, as that is exactly what the actor will be with the grievous error. 
BE CAREFUL NOT TO CHANGE THE FIRST NAME OF EVERY ACTOR TO MUCHO GROUCHO, HOWEVER! (Hint: update the record using a unique identifier.) */
update sakila.actor
set first_name = 'GROUCHO', last_name = 'MUCHO'
where actor_id = 172;

select *
from sakila.actor
where actor_id = 172;

# 5a. You cannot locate the schema of the address table. Which query would you use to re-create it?
select distinct table_schema, table_name
from information_schema.columns
where table_name = 'address';

/*create schema if not exists 'database';
use 'database';
create table if not exists 'database'.'address';*/


# 6a. Use JOIN to display the first and last names, as well as the address, of each staff member. Use the tables staff and address:
select a.first_name, a.last_name, b.address
from sakila.staff a
	join sakila.address b
		on a.address_id = b.address_id;

# 6b. Use JOIN to display the total amount rung up by each staff member in August of 2005. Use tables staff and payment.


select concat(b.first_name,' ',b.last_name) staff_name, a.total_amount as "$ total_amount (08/2005)"
from 
	(select staff_id, sum(amount) total_amount
	from sakila.payment
    where payment_date between str_to_date('2005/08/01', '%Y/%m/%d') and str_to_date('2005/09/01', '%Y/%m/%d')
	group by staff_id) a
		join sakila.staff b
			on a.staff_id = b.staff_id;

# 6c. List each film and the number of actors who are listed for that film. Use tables film_actor and film. Use inner join.
select a.film_id, a.title, count(*) number_of_actors
from sakila.film a
	inner join sakila.film_actor b
		on a.film_id = b.film_id
group by a.film_id, a.title;


# 6d. How many copies of the film Hunchback Impossible exist in the inventory system?
select count(*) number_of_invnetory
from 
	sakila.inventory a,
    sakila.film b
where a.film_id = b.film_id
and b.title = 'Hunchback Impossible';

# 6e. Using the tables payment and customer and the JOIN command, list the total paid by each customer. List the customers alphabetically by last name:
select c.customer_id, c.last_name, c.first_name, sum(p.amount) total_amount
from sakila.payment p
	join sakila.customer c
		on p.customer_id = c.customer_id
group by c.customer_id, c.last_name, c.first_name
order by c.last_name;


# 7a. The music of Queen and Kris Kristofferson have seen an unlikely resurgence. As an unintended consequence, 
# films starting with the letters K and Q have also soared in popularity. Use subqueries to display the titles of movies starting with the letters K and Q whose language is English.
select *
from sakila.film
where language_id = (select language_id from sakila.language where name ='English')
and substr(title,1,1) in ('K','Q');

# 7b. Use subqueries to display all actors who appear in the film Alone Trip.
select *
from sakila.actor
where actor_id in 
	(select actor_id
	 from sakila.film_actor
	 where film_id in (select film_id from sakila.film where title = 'Alone Trip'));


# 7c. You want to run an email marketing campaign in Canada, for which you will need the names and email addresses of all Canadian customers. Use joins to retrieve this information.
# Look for table that has country_id column
select distinct table_schema, table_name, column_name
from information_schema.columns
where upper(column_name) = 'COUNTRY_ID';

# City table has country_id column
select *
from sakila.city;

# Look for table that has city_id column
select distinct table_schema, table_name, column_name
from information_schema.columns
where upper(column_name) = 'CITY_ID';

# address table has city_id column
select *
from sakila.address;

select a.first_name, a.last_name, a.email
from sakila.customer a
	join sakila.address b on a.address_id = b.address_id
    join sakila.city c on b.city_id = c.city_id
    join sakila.country d on c.country_id = d.country_id
where upper(d.country) = 'CANADA';


# 7d. Sales have been lagging among young families, and you wish to target all family movies for a promotion. Identify all movies categorized as famiy films.
# Look for table that has film_id column
select distinct table_schema, table_name, column_name
from information_schema.columns
where upper(column_name) = 'FILM_ID';

select *
from sakila.film_category;

# Look for table that has category_id column
select distinct table_schema, table_name, column_name
from information_schema.columns
where upper(column_name) = 'CATEGORY_ID';

select *
from sakila.film
where film_id in(
	select film_id
	from sakila.film_category
	where category_id in (select category_id from sakila.category where name = 'Family'));

# 7e. Display the most frequently rented movies in descending order.
select *
from sakila.rental;

select *
from sakila.inventory;

select a. film_id, a.title, count(*) rental_freq
from sakila.film a
	inner join sakila.inventory b on a.film_id = b.film_id
    inner join sakila.rental c on b.inventory_id = c.inventory_id
group by a. film_id, a.title
order by count(*) desc;

# 7f. Write a query to display how much business, in dollars, each store brought in.
select a.*, b.total_amount
from sakila.store a,
(select staff_id, sum(amount) total_amount
from sakila.payment
group by staff_id) b
where a.manager_staff_id = b.staff_id;

# 7g. Write a query to display for each store its store ID, city, and country.
select a.store_id, c.city, d.country
from 
	sakila.store a,
    sakila.address b,
    sakila.city c,
    sakila.country d
where a.address_id = b.address_id
and b.city_id = c.city_id
and c.country_id = d.country_id;


# 7h. List the top five genres in gross revenue in descending order. (Hint: you may need to use the following tables: category, film_category, inventory, payment, and rental.)
select cat.name, sum(pay.amount) total_amt
from sakila.category cat
	inner join sakila.film_category fc on fc.category_id = cat.category_id
    inner join sakila.inventory inv on inv.film_id = fc.film_id
    inner join sakila.rental rent on rent.inventory_id = inv.inventory_id
    inner join sakila.payment pay on pay.rental_id = rent.rental_id
group by cat.name
order by sum(pay.amount) desc
limit 5;

# 8a. In your new role as an executive, you would like to have an easy way of viewing the Top five genres by gross revenue.
# Use the solution from the problem above to create a view. If you haven't solved 7h, you can substitute another query to create a view.
create view sakila.top_genre as 
select cat.name, sum(pay.amount) total_amt
from sakila.category cat
	inner join sakila.film_category fc on fc.category_id = cat.category_id
    inner join sakila.inventory inv on inv.film_id = fc.film_id
    inner join sakila.rental rent on rent.inventory_id = inv.inventory_id
    inner join sakila.payment pay on pay.rental_id = rent.rental_id
group by cat.name
order by sum(pay.amount) desc
limit 5;

# 8b. How would you display the view that you created in 8a?
select *
from sakila.top_genre;

# 8c. You find that you no longer need the view top_five_genres. Write a query to delete it.
drop view sakila.top_genre;