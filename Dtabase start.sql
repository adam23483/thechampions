CREATE table team (
		team_id int auto_increment,
        team_name varchar(100),
        league_postion int,
        league varchar(100),
        nation varchar(100),
        Primary KEY (team_id)
        );
        
CREATE table player (
		player_id int auto_increment,
        player_name varchar(100),
        team_id varchar(100),
        postion varchar(100),
        nation varchar(100),
        birthday date,
        height_inches int,
        Primary KEY (player_id)
        );

CREATE table player_performance(
		player_performance_id int auto_increment,
        player_id int,
        primary key  (player_performance_id),
        foreign key (player_id) references player(player_id)
        );
        
CREATE table shooting ( 
		shooting_id int auto_increment,
		player_id int,
        primary key  (shooting_id),
		foreign key (player_id) references player(player_id)
        );
        
CREATE table passing ( 
		passing_id int auto_increment,
		player_id int,
		primary key  (passing_id),
		foreign key (player_id) references player(player_id)
        );
        
CREATE table defending ( 
		defending_id int auto_increment,
		player_id int,
		primary key  (defending_id),
        foreign key (player_id) references player(player_id)
        );
        
CREATE table possession ( 
		possession_id int auto_increment,
		player_id int,
		primary key  (possession_id),
        foreign key (player_id) references player(player_id)
        );
CREATE table player_value (
		player_vlaue_id int auto_increment,
        player_id int,
        contract_signed date,
        contract_length int,
        contract_wage int,
        contract_ex boolean, 
        contract_ex_length int,
        transfer_value int,
        primary key  (player_vlaue_id),
        foreign key (player_id) references player(player_id)
);