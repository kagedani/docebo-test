-- Sum value of "Number of days with maximum 8-hour average ozone concentration over the
-- National Ambient Air Quality Standard" per year
SELECT 
	REPORTYEAR AS YEAR_COD,
	SUM(COALESCE(VALUE,0)) AS SUM_NBR_OF_DAYS_WITH_MAX_8HR_AVG_OZONE_CONCENTRATION
FROM AIR_QUALITY_MEASURES_ON_THE_NATIONAL_ENVIRONMENTAL_HEALTH_TRACK AQMOTNEHT 
WHERE MEASURENAME = 'Number of days with maximum 8-hour average ozone concentration over the National Ambient Air Quality Standard'
GROUP BY REPORTYEAR 
ORDER BY REPORTYEAR DESC

-- Year with max value of "Number of days with maximum 8-hour average ozone concentration
-- over the National Ambient Air Quality Standard" from year 2008 and later (inclusive)
SELECT YEAR_COD 
FROM 
(
	SELECT
		YEAR_COD,
		RANK() OVER (ORDER BY SUM_NBR_OF_DAYS_WITH_MAX_8HR_AVG_OZONE_CONCENTRATION DESC) AS RANK
	FROM 
	(
		SELECT 
			REPORTYEAR AS YEAR_COD,
			SUM(COALESCE(VALUE,0)) AS SUM_NBR_OF_DAYS_WITH_MAX_8HR_AVG_OZONE_CONCENTRATION 
		FROM AIR_QUALITY_MEASURES_ON_THE_NATIONAL_ENVIRONMENTAL_HEALTH_TRACK AQMOTNEHT 
		WHERE MEASURENAME = 'Number of days with maximum 8-hour average ozone concentration over the National Ambient Air Quality Standard'
		AND REPORTYEAR >= '2008'
		GROUP BY REPORTYEAR 
		ORDER BY REPORTYEAR DESC
	) A 
) B
WHERE B.RANK = 1

-- Max value of each measurement per state
SELECT 
	STATENAME,
	MEASUREID,
	MEASURENAME,
	MAX(VALUE) as MAX_VALUE_FOR_MEASURE
from AIR_QUALITY_MEASURES_ON_THE_NATIONAL_ENVIRONMENTAL_HEALTH_TRACK AQMOTNEHT 
group by MEASUREID, MEASURENAME, STATENAME 
ORDER by STATENAME, MEASUREID, MEASURENAME 

-- Average value of "Number of person-days with PM2.5 over the National Ambient Air Quality
-- Standard (monitor and modeled data)" per year and state in ascending order
-- VALUE = 0 removed to perform a better operation, but those values could also be included
SELECT 
	STATENAME,
	REPORTYEAR,
	AVG(VALUE) AS AVG_VALUE
FROM 
(
	SELECT MEASURENAME, STATENAME, REPORTYEAR, VALUE
	FROM AIR_QUALITY_MEASURES_ON_THE_NATIONAL_ENVIRONMENTAL_HEALTH_TRACK AQMOTNEHT 
	WHERE MEASURENAME = 'Number of person-days with PM2.5 over the National Ambient Air Quality Standard (monitor and modeled data)'
	AND VALUE <> 0
) A
GROUP BY STATENAME, REPORTYEAR
ORDER BY STATENAME, REPORTYEAR, AVG_VALUE ASC

-- State with the max accumulated value of "Number of days with maximum 8-hour average ozone
-- concentration over the National Ambient Air Quality Standard" overall years
SELECT 
	STATENAME 
FROM 
(
	SELECT 
		STATENAME,
		SUM(COALESCE(VALUE,0)) AS ACCULUMATED_VALUE_OVER_ALL_YEARS,
		RANK() OVER (ORDER BY SUM(COALESCE(VALUE,0)) DESC) AS RANK
	FROM AIR_QUALITY_MEASURES_ON_THE_NATIONAL_ENVIRONMENTAL_HEALTH_TRACK AQMOTNEHT 
	WHERE MEASURENAME = 'Number of days with maximum 8-hour average ozone concentration over the National Ambient Air Quality Standard'
	GROUP BY STATENAME 
	ORDER BY ACCULUMATED_VALUE_OVER_ALL_YEARS DESC
) A 
WHERE RANK = 1

-- Average value of "Number of person-days with maximum 8-hour average ozone concentration
-- over the National Ambient Air Quality Standard" in the state of Florida
SELECT AVG(VALUE) AS AVG_NBR_OF_PERSON_DAYS_WITH_MAX_8HR_AVG_OZONE_CONCENTRATION
FROM AIR_QUALITY_MEASURES_ON_THE_NATIONAL_ENVIRONMENTAL_HEALTH_TRACK AQMOTNEHT 
WHERE STATENAME = 'FLORIDA'
AND MEASURENAME = 'Number of person-days with maximum 8-hour average ozone concentration over the National Ambient Air Quality Standard'
AND VALUE <> 0 -- OPTIONAL CLAUSE

-- County with min "Number of days with maximum 8-hour average ozone concentration over the
-- National Ambient Air Quality Standard" per state per year
SELECT 
	A.COUNTYNAME, A.STATENAME, A.REPORTYEAR, A.MIN_VALUE
FROM 
(
	SELECT COUNTYNAME, STATENAME, REPORTYEAR, MIN(VALUE) AS MIN_VALUE
	FROM AIR_QUALITY_MEASURES_ON_THE_NATIONAL_ENVIRONMENTAL_HEALTH_TRACK AQMOTNEHT 
	WHERE MEASURENAME = 'Number of days with maximum 8-hour average ozone concentration over the National Ambient Air Quality Standard'
	AND VALUE <> 0 -- OPTIONAL CLAUSE
	GROUP BY COUNTYNAME, STATENAME, REPORTYEAR
	ORDER BY COUNTYNAME, STATENAME, REPORTYEAR
) A 
INNER JOIN 
(
	SELECT STATENAME, REPORTYEAR, MIN(VALUE) AS MIN_VALUE
	FROM AIR_QUALITY_MEASURES_ON_THE_NATIONAL_ENVIRONMENTAL_HEALTH_TRACK AQMOTNEHT 
	WHERE VALUE <> 0 -- OPTIONAL CLAUSE
	AND MEASURENAME = 'Number of days with maximum 8-hour average ozone concentration over the National Ambient Air Quality Standard'
	GROUP BY STATENAME, REPORTYEAR
	ORDER BY STATENAME, REPORTYEAR
) B 
ON A.STATENAME = B.STATENAME AND A.REPORTYEAR = B.REPORTYEAR AND A.MIN_VALUE = B.MIN_VALUE
