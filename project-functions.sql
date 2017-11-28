use project;

DELIMITER //
-- Suggested groups in order of occurance
CREATE PROCEDURE suggested_groups
(
user_id varchar(30)
)
BEGIN

SELECT g.name 
FROM (SELECT connected FROM connections WHERE user_id = owner) AS c
JOIN group_users gu ON (gu.user_username = c.connected)
JOIN groups g ON (gu.group_idgroup = g.idgroup)
GROUP BY g.name
ORDER BY count(gu.user_username) desc;

END //

-- Removes the removed from user_id
CREATE PROCEDURE drop_connection
(
user_id varchar(30),
removed varchar(30)
)
BEGIN

DELETE FROM connections
WHERE user_id = owner AND connected = removed;

END //

-- gives a users favorites
CREATE PROCEDURE view_connections
(
user_id varchar(30)
)
BEGIN

SELECT connected 
from connections
where user_id = owner;

END //

-- adds a person to connections
CREATE PROCEDURE add_connection
(
user_id varchar(30),
added varchar(30)
)
BEGIN

INSERT INTO connections (owner, connected)
VALUES (user_id, added);

END //

-- user joins a group
CREATE PROCEDURE join_group
(
user_id varchar(30),
group_id int
)
BEGIN

INSERT INTO connections (group_idgroup, user_username)
VALUES (user_id, group_id);

END //

-- user becomes an admin of a group
CREATE PROCEDURE add_admin
(
user_id varchar(30),
group_id int
)
BEGIN

INSERT INTO gorup_admin (group_idgroup, user_username)
VALUES (group_id, user_id);

END//

-- adds a member of users who is not an admin to the admins of a group if there is one
CREATE PROCEDURE force_add_admin
(
group_id int
)
BEGIN
DECLARE new_admin varchar(30);

SELECT user_username  into new_admin FROM group_users
WHERE group_id = group_idgroup AND
user_username NOT IN (SELECT user_username FROM group_admin
WHERE group_id = group_idgroup)
LIMIT 1;

IF (new_admin IS NOT NULL)
THEN CALL add_admin(new_admin, group_id);
END IF;

END //

-- remove an admin of a group, if admin is the only member of the group, are forced to
-- be the admin
CREATE PROCEDURE rm_admin
(
user_id varchar(30),
group_id int
)
BEGIN

DELETE FROM group_admin 
WHERE user_id = user_username AND group_id = group_idgroup;

-- There must always be an admin in a group check if no more admins
IF ((SELECT count(*) FROM goup_admin WHERE group_id = group_idgroup) = 0)
	-- If there are no members in group delete it
    THEN IF ((SELECT count(*) FROM group_users WHERE group_id = group_idgroup) = 0)
			THEN DELETE FROM groups where idgroup = group_id;
            
            -- otherwise force a memer of the group to be an admin
            ELSE call force_add_admin(group_id);
		END IF;		
END IF;
END //

-- user leaves a group, and is no longer an admin
CREATE PROCEDURE leave_group
(
user_id varchar(30),
group_id int
)
BEGIN
DELETE FROM group_users WHERE user_username = user_id AND group_id = group_idgroup;
END //


-- when a user is removed from a group they are no longer an admin
-- need to call
CREATE TRIGGER removed_group AFTER DELETE ON group_users
FOR EACH ROW
BEGIN

CALL rm_admin(OLD.user_username, OLD.group_idgroup);

END //

-- login returns true if credentials match
CREATE PROCEDURE login
(
user_id varchar(30),
pass varchar(45)
)
BEGIN
declare chk_pass varchar(45);
SELECT password into chk_pass FROM users where user_id = username;
IF (chk_pass is not NULL and check_pass = pass)
then select TRUE;
ELSE select FALSE;
END IF;
END//

-- create new user, gives true if user is sucessfully created
CREATE PROCEDURE new_user
(
user_id varchar(30),
pass varchar(45)
)
BEGIN
IF ((select count(username) from users where username = user_id) = 0)
THEN
INSERT INTO users (username, password)
VALUES (user_id, pass);
SELECT TRUE;
ELSE SELECT FALSE;
END IF;

END //


-- delete account
CREATE PROCEDURE del_user
(
user_id varchar(30)
)
BEGIN

DELETE FROM users WHERE user_id = username;

END // 

-- remove the associated info
CREATE TRIGGER del_user_info  AFTER DELETE ON users
FOR EACH ROW
BEGIN
DELETE FROM conenctions WHERE OLD.username = owner OR connected = OLD.username;
DELETE FROM co_ops WHERE OLD.username = user_username;
DELETE FROM course WHERE OLD.username = user_username;
DELETE FROM tag_user WHERE OLD.username = user_username;
DELETE FROM research WHERE OLD.username = user_username;
DELETE FROM major WHERE OLD.username = user_username;
DELETE FROM minor WHERE OLD.username = user_username;
DELETE FROM study_abroad WHERE OLD.username = user_username;
DELETE FROM group_users WHERE OLD.username = user_username;
END //

-- gets the emails of a groups users 
CREATE PROCEDURE group_emails
(
group_id int
)
BEGIN

SELECT email
from users join group_users on (users.username = group_users.user_username)
where group_users.group_idgroup = group_id;

END //

-- create group
CREATE PROCEDURE new_group
(
group_name varchar(45),
about text
)
BEGIN

INSERT INTO groups (name, description)
VALUES (group_name, about);

END //

-- get user's co-ops
CREATE PROCEDURE get_co_ops
(
user_id varchar(30)
)
BEGIN

SELECT start, end, company, description
 FROM co_ops 
 WHERE user_id = co_ops.user_username;

END //

-- get user's courses
CREATE PROCEDURE get_courses
(
user_id varchar(30)
)
BEGIN

SELECT Name, professor, semester 
FROM course 
WHERE user_id = courses.user_username;

END //

-- get user's groups
CREATE PROCEDURE get_groups
(
user_id varchar(30)
)
BEGIN

SELECT groups.name, groups.description
FROM group_users join groups on (groups.idgroup = group_users.group_idgroup) 
WHERE user_id = group_users.user_username;

END //

-- get user's majors
CREATE PROCEDURE get_major
(
user_id varchar(30)
)
BEGIN

SELECT name
FROM major 
WHERE user_id = user_username;

END //

-- get user's minors
CREATE PROCEDURE get_minors
(
user_id varchar(30)
)
BEGIN

SELECT name
FROM minor 
WHERE user_id = user_username;

END //

-- get user's research
CREATE PROCEDURE get_research
(
user_id varchar(30)
)
BEGIN

SELECT start, end, professor, decription
FROM minor 
WHERE user_id = user_username;

END //

--  edit groups


-- delete a co-op from a user
CREATE PROCEDURE del_co_op
(
user_id varchar(30),
old_start date
)
BEGIN

 DELETE FROM co_ops 
 WHERE user_id = co_ops.user_username AND old_start = co_ops.start;

END //

-- delete a course from a user
CREATE PROCEDURE del_courses
(
id varchar(30)

)
BEGIN

DELETE FROM course
WHERE id = course.idcourse;

END //

-- delete a major from a user
CREATE PROCEDURE del_major
(
user_id varchar(30),
m_name varchar(45)
)
BEGIN

DELETE FROM major 
WHERE user_id = user_username && name = m_name;

END //

-- delete a minor from a user
CREATE PROCEDURE del_minor
(
user_id varchar(30),
m_name varchar(45)
)
BEGIN

DELETE FROM minor 
WHERE user_id = user_username && name = m_name;

END //

-- delete a users research
CREATE PROCEDURE del_research
(
user_id varchar(30),
sdate date
)
BEGIN

DELETE FROM research
WHERE user_id = user_username && research.start = sdate;

END //

-- Adds a minor to a user
CREATE PROCEDURE add_minor
(
user_id varchar(30),
minor varchar(45)
)
BEGIN

INSERT INTO minor (name, user_username)
VALUES (minor, user_id);

END //

-- Adds a major to a user
CREATE PROCEDURE add_major
(
user_id varchar(30),
major varchar(45)
)
BEGIN

INSERT INTO major (name, user_username)
VALUES (major, user_id);

END //
-- Adds a co-op to a user
CREATE PROCEDURE add_co_op
(
user_id varchar(30),
sdate date,
edate date,
comp varchar(45),
about text
)
BEGIN

INSERT INTO co_ops (start, end, user_username, company, description)
VALUES (sdate, edate, user_id, comp, about);

END //

-- Adds a course to a user
CREATE PROCEDURE add_course
(
user_id varchar(30),
title varchar(45),
sem date,
prof varchar(45)
)
BEGIN

INSERT INTO course (Name, professor, semester, user_username)
VALUES (title, prof, sem, user_id);

END //

-- Adds research to a user
CREATE PROCEDURE add_research
(
user_id varchar(30),
sdate date,
edate date,
prof varchar(45),
about text
)
BEGIN

INSERT INTO research (start, end, professor, descrption, user_username)
VALUES (sdate, edate, prof, about, user_id);

END //

-- Adds a study abroad to a user
CREATE PROCEDURE add_study_abroad
(
user_id varchar(30),
sdate date,
edate date,
uni varchar(45),
loc varchar(45)
)
BEGIN

INSERT INTO study_abroad (country, start, end, university, user_username)
VALUES (loc, sdate, edate, uni, user_id);

END //

-- update user's basic info
CREATE PROCEDURE update_user
(
user_id varchar(30),
disp_name varchar(45),
descr text,
grad int,
pic blob,
mail varchar(45),
num int
)
BEGIN

UPDATE users 
SET Name = disp_name, Description = descr, gradYear = grad, Picture = pic,
 email = mail, phome = num
 WHERE username = user_id;
 
 END //
 
 -- updates a groups infrmaton
 CREATE PROCEDURE update_group
 (
 group_id int,
 gr_name varchar(45),
 about text,
 pic blob
 )
 BEGIN
 
 UPDATE groups
 SET name = gr_name, description = about, picture = pic
 WHERE idgroup = griup_id;
 
 END //
 
 -- Add a tag to a user
 CREATE PROCEDURE add_tag_user
 (
 tag varchar(45),
 user_id varchar(30)
 )
 BEGIN
 
 INSERT INTO tag_user  (name, user_username)
 VALUES (tag, user_id);
 
 END //
 
 -- Remove a tag from a user
 CREATE PROCEDURE del_tag_user
 (
 tag varchar(45),
 user_id varchar(30)
 )
 BEGIN
 
 DELETE FROM tag_user
 WHERE user_username = user_id AND tag = name;
 
 END //
 
 -- add a tag to a group
 CREATE PROCEDURE add_tag_group
 (
 tag varchar(45),
 groupid int
 ) 
BEGIN 

INSERT INTO tag_group (name, group_idgroup)
VALUES (tag, groupid);

END //

-- remove a tag from a group
CREATE PROCEDURE del_tag_group
(
tag varchar(45),
groupid int
)
BEGIN

DELETE FROM tag_group
WHERE user_username = user_id AND tag = name;

END //
 
-- search for user by tag, will return results where tag contains search term
-- order by tags closest to the search term
CREATE PROCEDURE search_user_tag
(
tag varchar(45)
)
BEGIN

SELECT *
FROM users u JOIN tag_user  t ON (u.username = t.users_username)
WHERE t.name LIKE concat("%", tag, "%")
ORDER BY t.name / tag;

END //

-- search for groups by tag, will return results where tag contains search term
-- order by tags closest to the search term
CREATE PROCEDURE search_group_tag
(
tag varchar(45)
)
BEGIN

SELECT *
FROM groups g JOIN tag_gorup  t ON (g.idgroup = t.group_idgroup)
WHERE t.name LIKE concat("%", tag, "%")
ORDER BY t.name / tag;

END //
