SELECT
  origin,            -- Selects the country of origin of each band
  SUM(fans) nb_fans  -- Sums the number of fans for all bands from the same country
FROM
  metal_bands        -- Source table containing information about bands and their fans
GROUP BY
  origin             -- Groups the results by the country of origin
ORDER BY
  nb_fans DESC       -- Orders the results in descending order of total fans
