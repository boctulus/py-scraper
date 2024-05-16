CREATE TABLE robot_execution (
    id INT AUTO_INCREMENT PRIMARY KEY,
    execution_datetime DATETIME NOT NULL,
    order_file VARCHAR(255) NOT NULL,
    robot_status ENUM('idle', 'running', 'completed', 'error') NOT NULL,
	error_msg VARCHAR(255) NULL,
    last_screenshot VARCHAR(255)
);

