SELECT det.*, sgq.*, zp.*
FROM dr3.all_dr3 as det
JOIN dr3.vac_star_galaxy_quasar as sgq ON (det.ID = sgq.ID)
JOIN dr3.vac_photoz as zp ON (det.ID = zp.ID)
WHERE 1 = CONTAINS( POINT('ICRS', det.ra, det.dec), CIRCLE('ICRS', 159.17, -27.524, 5*1.5744)) and det.r_auto < 21
and sgq.PROB_GAL > 0.7
and det.field = 'HYDRA-0043'
