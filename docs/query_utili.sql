.headers on
.tables

# pesi categorie
select a.id, a.description, w.weight, c.description from activity a join weight_category w on a.id = w.activity_id join category c on w.category_id = c.id;