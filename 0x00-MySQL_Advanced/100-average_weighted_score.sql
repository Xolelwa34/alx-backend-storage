-- script that creates a stored procedure 

DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser (IN user_id INT)
BEGIN
    DECLARE total_score FLOAT;
    DECLARE total_weight INT;
    DECLARE weighted_avg FLOAT;
    
    -- Initialize variables
    SET total_score = 0;
    SET total_weight = 0;
    
    -- Calculate total weighted score
    SELECT SUM(c.score * p.weight), SUM(p.weight)
    INTO total_score, total_weight
    FROM corrections c
    INNER JOIN projects p ON c.project_id = p.id
    WHERE c.user_id = user_id;
    
    -- Calculate weighted average
    IF total_weight > 0 THEN
        SET weighted_avg = total_score / total_weight;
    ELSE
        SET weighted_avg = 0;
    END IF;
    
    -- Update user's average_score
    UPDATE users
    SET average_score = weighted_avg
    WHERE id = user_id;
    
END //

DELIMITER ;
