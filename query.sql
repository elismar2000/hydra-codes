#Query que usei pra baixar a tabela principal de photo-zs que eu utilizo:
SELECT det.*, sgq.*, zp.*
FROM dr3.all_dr3 as det
JOIN dr3.vac_star_galaxy_quasar as sgq ON (det.ID = sgq.ID)
JOIN dr3.vac_photoz as zp ON (det.ID = zp.ID)
WHERE 1 = CONTAINS( POINT('ICRS', det.ra, det.dec), CIRCLE('ICRS', 159.17, -27.524, 5*1.5744)) and det.r_auto < 21
and sgq.PROB_GAL > 0.7
and det.field = 'HYDRA-0043'


#Query para baixar dados do iDR4 (Stripe82):
SELECT
det.ID, det.RA, det.DEC, u.u_PStotal, j0378.J0378_PStotal, j0395.J0395_PStotal,
j0410.J0410_PStotal, j0430.J0430_PStotal, g.g_PStotal, j0515.J0515_PStotal,
r.r_PStotal, j0660.J0660_PStotal, i.i_PStotal, j0861.J0861_PStotal, z.z_PStotal,
u.e_u_PStotal, j0378.e_J0378_PStotal, j0395.e_J0395_PStotal,
j0410.e_J0410_PStotal, j0430.e_J0430_PStotal, g.e_g_PStotal,
j0515.e_J0515_PStotal, r.e_r_PStotal, j0660.e_J0660_PStotal,
i.e_i_PStotal, j0861.e_J0861_PStotal, z.e_z_PStotal, det.s2n_DET_auto,
det.SEX_FLAGS_DET, sgq.PROB_GAL, sgq.CLASS, pz.odds, pz.zml

FROM
idr4_dual.idr4_detection_image AS det
JOIN idr4_dual.idr4_dual_u     AS u     ON (det.ID = u.ID)
JOIN idr4_dual.idr4_dual_j0378 AS j0378 ON (det.ID = j0378.ID)
JOIN idr4_dual.idr4_dual_j0395 AS j0395 ON (det.ID = j0395.ID)
JOIN idr4_dual.idr4_dual_j0410 AS j0410 ON (det.ID = j0410.ID)
JOIN idr4_dual.idr4_dual_j0430 AS j0430 ON (det.ID = j0430.ID)
JOIN idr4_dual.idr4_dual_g     AS g     ON (det.ID = g.ID)
JOIN idr4_dual.idr4_dual_j0515 AS j0515 ON (det.ID = j0515.ID)
JOIN idr4_dual.idr4_dual_r     AS r     ON (det.ID = r.ID)
JOIN idr4_dual.idr4_dual_j0660 AS j0660 ON (det.ID = j0660.ID)
JOIN idr4_dual.idr4_dual_i     AS i     ON (det.ID = i.ID)
JOIN idr4_dual.idr4_dual_j0861 AS j0861 ON (det.ID = j0861.ID)
JOIN idr4_dual.idr4_dual_z     AS z     ON (det.ID = z.ID)
JOIN idr4_vacs.idr4_star_galaxy_quasar AS sgq ON (det.ID = sgq.ID)
JOIN idr4_vacs.idr4_photoz AS pz ON (det.ID = pz.ID)

WHERE
(det.Field = '{value.field}')
AND (det.s2n_DET_auto > 3)
AND (sgq.CLASS = 2)
AND (g.g_PStotal < 30)
AND (r.r_PStotal < 30)
AND (i.i_PStotal < 30)
AND (z.z_PStotal < 30)



#Pra fazer o crossmatch com a tabela dos spec-zs:
java -jar stilts.jar tskymatch2 in1=Fields_S82/S82.csv in2=tables_speczs/SpecZ_Catalogue_20220701.csv out=Fields_S82/S82_matched.csv ra1=RA dec1=DEC ra2=RA dec2=DEC error=3



#Pra baixar o g_petro e r_petro do Stripe82:
SELECT
det.ID, g.g_petro, r.r_petro

FROM
idr4_dual.idr4_detection_image AS det
JOIN idr4_dual.idr4_dual_g     AS g     ON (det.ID = g.ID)
JOIN idr4_dual.idr4_dual_r     AS r     ON (det.ID = r.ID)

WHERE
(det.Field = '{value.field}')
AND (g.g_petro < 30)
AND (r.r_petro < 30)



#Pra baixar dados de Hydra do iDR4:
SELECT
det.ID, det.RA, det.DEC, sgq.PROB_GAL, sgq.CLASS, pz.odds, pz.zml,
g.g_petro, r.r_petro

FROM
idr4_dual.idr4_detection_image AS det
JOIN idr4_vacs.idr4_star_galaxy_quasar AS sgq ON (det.ID = sgq.ID)
JOIN idr4_vacs.idr4_photoz AS pz ON (det.ID = pz.ID)
JOIN idr4_dual.idr4_dual_g     AS g     ON (det.ID = g.ID)
JOIN idr4_dual.idr4_dual_r     AS r     ON (det.ID = r.ID)

WHERE
(det.Field = '{value.field}')
AND (g.g_petro < 30)
AND (r.r_petro < 30)


#Dados do Legacy Survey (DECam)
SELECT TOP 500000

ls_dr9.tractor.objid, ls_dr9.tractor.ra, ls_dr9.tractor.dec, ls_dr9.tractor.mag_g, ls_dr9.tractor.mag_r, ls_dr9.tractor.mag_z, ls_dr9.tractor.dered_mag_g,
ls_dr9.tractor.dered_mag_r,  ls_dr9.tractor.dered_mag_z, ls_dr9.tractor.ebv, ls_dr9.tractor.type, ls_dr9.photo_z.z_spec
FROM ls_dr9.tractor,  ls_dr9.photo_z

WHERE 't' = Q3C_RADIAL_QUERY(ra, dec, 159.17, -27.524, 7.872)


#Dados do Gaia:
SELECT
a.source_id, a.ra, a.dec, a.parallax

FROM gaiadr3.gaia_source AS a

WHERE 1 = CONTAINS( POINT('ICRS', a.ra, a.dec), CIRCLE('ICRS', 159.17, -27.524, 5*1.5744))


#Dados do Gaia (amostra + pura de galáxias)
SELECT
gc.source_id

FROM gaiadr3.galaxy_candidates AS gc

WHERE (radius_sersic IS NOT NULL OR
classlabel_dsc_joint='galaxy' OR
vari_best_class_name='GALAXY')


#Galaxias do Gaia na região de Hydra-Centaurus:
SELECT gc.source_id, a.ra, a.dec

FROM gaiadr3.galaxy_candidates AS gc
JOIN gaiadr3.gaia_source AS a ON (a.source_id = gc.source_id)

WHERE
a.ra > 140.0 AND a.ra < 185.0 AND
a.dec > (-50.0)AND a.dec < (-15.0)
