with imageset as
(
select row_number() over (partition by i.image_id order by i.image_seq desc) as 'RowNumber',
		i.image_id, i.image_seq from sysadm.picture_it i
)

select (case when i.image_seq is null then '0' else i.image_seq end) as 'Image Sequence', x.image_seq as 'Previous Image Sequence', k.intake_cond, k.intake_date, k.crossing, k.animal_id, a.animal_type, a.s_n_comp_date, a.s_n_due_date, a.sex, a.animal_name, a.dob, k.jurisdiction, a.primary_color, a.secondary_color, a.primary_breed, a.secondary_breed, k.outcome_type, k.outcome_date, p.first_name, p.last_name
 from sysadm.kennel k
inner join sysadm.animal a
on a.animal_id = k.animal_id
left join sysadm.person p
on k.owner_id = p.person_id
left join imageset i
on k.animal_id = i.image_id
left join sysadm.straymapper_image_counter x
on x.animal_id = k.animal_id
where i.RowNumber <= 1 
and k.intake_date between DATEADD(day, DATEDIFF(day,14,getdate()), 0) and getdate()
		and not (k.kennel_no in ('FOUND', 'HOME QUAR'))
		and a.animal_type in ('DOG', 'CAT')
		and k.intake_type = 'STRAY'
		and k.intake_cond != 'DEAD'
		
UNION

select (case when i.image_seq is null then '0' else i.image_seq end) as 'Image Sequence', x.image_seq as 'Previous Image Sequence', k.intake_cond, k.intake_date, k.crossing, k.animal_id, a.animal_type, a.s_n_comp_date, a.s_n_due_date, a.sex, a.animal_name, a.dob, k.jurisdiction, a.primary_color, a.secondary_color, a.primary_breed, a.secondary_breed, k.outcome_type, k.outcome_date, p.first_name, p.last_name
 from sysadm.kennel k
inner join sysadm.animal a
on a.animal_id = k.animal_id
left join sysadm.person p
on k.owner_id = p.person_id
left join imageset i
on k.animal_id = i.image_id
left join sysadm.straymapper_image_counter x
on x.animal_id = k.animal_id
where i.image_id is null
and k.intake_date between DATEADD(day, DATEDIFF(day,14,getdate()), 0) and getdate()
		and not (k.kennel_no in ('FOUND', 'HOME QUAR'))
		and a.animal_type in ('DOG', 'CAT')
		and k.intake_type = 'STRAY'
		and k.intake_cond != 'DEAD'
		order by k.animal_id asc