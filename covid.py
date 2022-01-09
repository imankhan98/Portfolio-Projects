SELECT *
FROM `covid-project-337022.covid_deaths.covid_deaths` 
ORDER BY 3,4

SELECT *
FROM `covid-project-337022.covid_vaccinations.CovidVaccinations`
ORDER BY 3,4

SELECT distinct (continent), count (continent)
from `covid-project-337022.covid_deaths.covid_deaths`
group by (continent)

-- Data I will be using
SELECT location, date, total_cases, new_cases, total_deaths, population
FROM `covid-project-337022.covid_deaths.covid_deaths` 
ORDER BY 1,2

-- Looking at Total Cases vs Total Deaths
-- Shows likelihood of contracting Covid in your country 
SELECT location, date, total_cases, total_deaths, (total_deaths/total_cases)*100 AS death_percentage
FROM `covid-project-337022.covid_deaths.covid_deaths` 
WHERE location like '%States%'
and continent is not null 
ORDER BY 1,2

-- Looking at Total Cases vs Population
-- Shows what percentage of popluation contracted Covid
SELECT location, date, population, total_cases, (total_cases/population )*100 AS percent_population_infected
FROM `covid-project-337022.covid_deaths.covid_deaths` 
WHERE location like '%States%'
ORDER BY 1,2

-- Looking at countires with the highest infection rate vs population
SELECT location, population, MAX (total_cases) AS highest_infection_count , MAX ((total_cases/population))*100 AS percent_population_infected
FROM `covid-project-337022.covid_deaths.covid_deaths`
GROUP BY location, population
ORDER BY 4 desc 

-- Showing countries with the highest death count per population
SELECT location, MAX(cast(total_deaths as int)) AS total_death_count
FROM `covid-project-337022.covid_deaths.covid_deaths`
WHERE continent is not null
GROUP BY location
ORDER BY total_death_count desc 

-- Grouping by continent instead of country (location)
-- Showing continents with the highest death count per population
SELECT continent, MAX(cast(total_deaths as int)) AS total_death_count
FROM `covid-project-337022.covid_deaths.covid_deaths`
WHERE continent is not null
GROUP BY continent 
ORDER BY total_death_count desc 

-- Global Numbers every day
SELECT date, SUM(new_cases) as total_cases, SUM(cast(new_deaths as int)) as total_deaths, SUM(cast(new_deaths as int))/SUM(new_cases)*100 as death_percentage
FROM `covid-project-337022.covid_deaths.covid_deaths` 
WHERE continent is not null 
GROUP BY date
ORDER BY 1,2

-- Showing total cases worldwide vs total deaths and death percentage
SELECT SUM(new_cases) as total_cases, SUM(cast(new_deaths as int)) as total_deaths, SUM(cast(new_deaths as int))/SUM(new_cases)*100 as death_percentage
FROM `covid-project-337022.covid_deaths.covid_deaths` 
WHERE continent is not null 
--GROUP BY date
ORDER BY 1,2

-- Looking at total population vs total vaccinations
SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
SUM(cast(vac.new_vaccinations as int)) OVER (PARTITION BY dea.location ORDER BY dea.location, dea.date) as rolling_people_vaccinated
FROM `covid-project-337022.covid_deaths.covid_deaths` dea
JOIN `covid-project-337022.covid_vaccinations.CovidVaccinations` vac
    on dea.location = vac.location
    and dea.date = vac.date
WHERE dea.continent is not null 
ORDER BY 2,3

-- USE CTE (Common Table Expression)

WITH PopvsVac (continent, location, date, population, new_vaccinations, rolling_people_vaccinated)
as
(
SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
SUM(cast(vac.new_vaccinations as int)) OVER (PARTITION BY dea.location ORDER BY dea.location, dea.date) as rolling_people_vaccinated
FROM `covid-project-337022.covid_deaths.covid_deaths` dea
JOIN `covid-project-337022.covid_vaccinations.CovidVaccinations` vac
    on dea.location = vac.location
    and dea.date = vac.date
WHERE dea.continent is not null 
)






