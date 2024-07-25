DELIMITER $$

USE AT_Dev$$

DROP PROCEDURE IF EXISTS TransactionSearch$$

CREATE PROCEDURE TransactionSearch(
    IN p_TransactionType VARCHAR(25),
    IN p_AccountNumber VARCHAR(10),
    IN p_AccountHolderName VARCHAR(50),
    IN p_AccountType VARCHAR(10)
)
BEGIN
    SELECT 
        t.Id,
        t.TransactionDate,
        t.Amount,
        t.Description,
        t.TransactionType,
        a.AccountNumber,
        a.AccountHolderName,
        a.AccountType,
        a.Balance
    FROM 
        AT_Dev.Transaction t
    INNER JOIN 
        AT_Dev.AccountDetails a ON t.AccountId = a.AccountNumber
    WHERE
        (p_TransactionType IS NULL OR t.TransactionType = p_TransactionType) AND
        (p_AccountNumber IS NULL OR a.AccountNumber = p_AccountNumber) AND
        (p_AccountHolderName IS NULL OR a.AccountHolderName = p_AccountHolderName) AND
        (p_AccountType IS NULL OR a.AccountType = p_AccountType);
END$$

DELIMITER ;
