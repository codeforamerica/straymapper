using System;

namespace StrayMapperExporter
{
    public static class Credentials
    {
        public static string connectionString = ""; //Sql Server Connection String

        public static string accessKey = ""; //Amazon S3 access key
        public static string secretAccessKey = ""; //Amazon S3 secret access key
        public static string bucketName = ""; //Amazon S3 bucket name
        public static string emailServer = ""; //Your e-mail server (in this case it's an Exchange server)
        public static int port = 25; //this can be any port, you usually can leave this blank
        public static string imageDir = ""; //the directory you save images to
        public static string webhookEmail = ""; //if you're sending this data to a webhook account (like MailGun) it goes here
        public static string fromAddress = ""; //your e-mail address
        public static string baseDirectory = ""; //base directory for all of your straymapper stuff
        public static string csvRoot = ""; //where you'll keep the csv files
       
        #region sqlQuery
        //thrown in this class to not clog up the main code
        public static string sqlQuery = @"
            drop table tempSM;
            create table tempSM
            (image_id varchar(50),
             image_seq smallint,
             image_bool varchar(5));


            with kitten as (select ROW_NUMBER() OVER ( PARTITION BY image_id order by image_seq DESC) as 'RowNumber',
                image_id, image_seq
                from sysadm.picture_it where image_id is not null and image_resolution = 'Detail')

                        insert into tempSM(image_id, image_seq, image_bool)
                        select k.image_id, k.image_seq, (case when k.image_seq > si.image_seq then 'TRUE' else 'FALSE' end)
                        from kitten k
                            left join sysadm.straymapper_image si
                            on si.image_id = k.image_id
                            where RowNumber = 1
                            and k.image_id in
                            (select k.animal_id
                            from sysadm.kennel k
                                inner join sysadm.animal a
                                on a.animal_id = k.animal_id
                                left join sysadm.person p
                                on p.person_id = k.owner_id
                                    where a.animal_type in ('DOG', 'CAT')
                                        and k.intake_date between DATEADD(day, DATEDIFF(day,14,getdate()), 0) and getdate()
                                        and not (k.kennel_no in ('FOUND', 'HOME QUAR'))
                                        and k.intake_type = 'STRAY'
                                        and k.intake_cond != 'DEAD');


            select cast (k.intake_date as DATE) as 'Intake Date',
                                 (case when k.crossing is null then k.jurisdiction + ', TX' else k.crossing + ' ' + k.jurisdiction + ', TX' end)
	                                     as 'Found Location',
                                            k.intake_cond as 'Intake Condition', 
		                                    k.animal_id as 'Animal ID', 
		                                    (case when
			                                    DATEDIFF(d, a.dob, k.intake_date) <= 120
				                                    and a.animal_type = 'CAT'
					                                    then 'KITTEN'
			                                      when
			                                    DATEDIFF(d, a.dob, k.intake_date) > 120
				                                    and a.animal_type = 'CAT'
					                                    then 'CAT'
			                                      when
			                                    DATEDIFF(d, a.dob, k.intake_date) <= 120
				                                    and a.animal_type = 'DOG'
					                                    then 'PUPPY'
			                                      when
			                                    DATEDIFF(d, a.dob, k.intake_date) > 120
				                                    and a.animal_type = 'DOG'
					                                    then 'DOG'
			                                     when
			                                     a.dob is null
				                                    and a.animal_type = 'CAT'
					                                    then 'CAT'
			                                     when
			                                     a.dob is null
				                                    and a.animal_type = 'DOG'
					                                    then 'DOG'
					                                    end) as 'Animal Type',
                                                (case
                                                 when a.sex in ('M', 'N') then 'MALE'
                                                 when a.sex in ('S', 'F') then 'FEMALE'
                                                 when a.sex = 'U' then 'UNKNOWN' end)
                                                as 'Sex',
		                                        (case 
			                                     when
				                                    a.sex = 'S' then 'YES'
		                                         when
				                                    a.sex = 'N' then 'YES'
			                                     when
				                                    a.sex = 'F' then 'NO'
			                                     when
				                                    a.sex = 'M' then 'NO'
			                                     when
				                                    a.sex = 'U' then 'UNKNOWN'
				                                    end) as 'Spayed/Neutered?',
			                                    (case
			                                     when
				                                    a.animal_name is not null
				                                    and a.animal_name like '*%'
				                                    then LTRIM(SUBSTRING(a.animal_name,2,LEN(a.animal_name)))
		                                          when
				                                    a.animal_name is not null
				                                    and not (a.animal_name) like '*%'
				                                    then a.animal_name
			                                      else
				                                    ''
			                                      end) as 'Name',
			                                      DATEDIFF(dd, a.dob, k.intake_date) as 'Days Old',
			                                      RTRIM((a.primary_color + ' ' + isnull(a.secondary_color, '') + ' '
				                                    + a.primary_breed + ' ' + isnull(a.secondary_breed, '')))
					                                    as 'Description',
			                                       k.outcome_type as 'Outcome Type',
			                                       (cast (k.outcome_date as DATE)) as 'Outcome Date',
			                                       (case when
				                                    k.outcome_type = 'TRANSFER'
					                                    and p.first_name = 'APA'
					                                    then 'APA Rescue'
				                                    when
				                                    k.outcome_type = 'TRANSFER'
					                                    and p.person_id = 'P070962'
					                                    then 'Austin Humane Society'
				                                    when k.outcome_type = 'TRANSFER'
				                                      and not (p.person_id in ('P083529', 'P070962'))
				                                        then LTRIM(sysadm.ToProperCase(p.first_name) + ' ' + sysadm.ToPropercase(p.last_name))
				                                        else ''
				                                     end) as 'Transferred To',
				                                     (case
				                                     when sm.image_bool = 'TRUE' then 'New Image Available' else null end)  as 'Image Updated'      
                                    from sysadm.kennel k
	                                    inner join sysadm.animal a
	                                    on a.animal_id = k.animal_id
	                                    left join sysadm.person p
	                                    on p.person_id = k.owner_id
										left join sysadm.tempSM sm
										on sm.image_id = k.animal_id
		                                    where a.animal_type in ('DOG', 'CAT')
			                                    and k.intake_date between DATEADD(day, DATEDIFF(day,14,getdate()), 0) and getdate()
			                                    and not (k.kennel_no in ('FOUND', 'HOME QUAR'))
			                                    and k.intake_type = 'STRAY'
			                                    and k.intake_cond != 'DEAD'
			                                    order by k.animal_id asc;
			             
			            

";
        #endregion



    }
}