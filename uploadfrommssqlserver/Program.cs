using System;
using System.Data;
using System.Drawing;
using System.Text;
using Amazon.S3;
using Amazon.S3.Model;   // These use the AWS.Extensions and AWSSDK .dll files. These are freely available through Amazon's
using System.IO;         // S3 .NET package.
using System.Data.SqlClient;
using System.Net.Mail;

namespace StrayMapperExporter
{
    static class Program
    {
        [STAThread]
        static void Main()
        {
            DirectoryClearer();
            CSVExport();
            ImageWriterExecutor();
            StrayMapperImageUploader();
            ImageTrackerUpdate();
            SendCSVFile();
        }

      static string filename;
      //Most of the strings used here are concealed in the Credentials class
	  
      static void CSVExport()
	  // Creates the datatable that will export to the CSV then calls the CSV method
        {
            try
            {
                SqlConnection con = new SqlConnection(Credentials.connectionString);
                con.Open();
                SqlDataAdapter da = new SqlDataAdapter(Credentials.sqlQuery, con);
                DataTable dt = new DataTable();
                da.Fill(dt);
                ToCSV(dt, ",");
                con.Close();
            }

            catch (Exception error)
            {
                SendMeExceptionError(error);
            }


        }

      static void ToCSV(DataTable table, string delimiter)
	 {
            try
            {
                StringBuilder result = new StringBuilder();

                foreach (DataColumn column in table.Columns)
                {
                    string itemAsString = column.ToString();
                    itemAsString = itemAsString.Replace("\"", "\"\"");
                    itemAsString = "\"" + itemAsString + "\"";
                    result.Append(itemAsString + delimiter);
                }
                result.Remove(--result.Length, 0);
                result.Append(Environment.NewLine);

                foreach (DataRow row in table.Rows)
                {

                    foreach (object item in row.ItemArray)
                    {
                       
                        if (item is System.DateTime)
                        {
                            string itemAsString = item.ToString();
                            itemAsString = itemAsString.Replace("\"", "\"\"").Replace(" 12:00:00 AM", "");
                            result.Append(itemAsString + delimiter);
                        }
                        else
                        {

                            string itemAsString = item.ToString();
                            itemAsString = itemAsString.Replace("\"", "\"\"").Replace(" 12:00:00 AM", "").Replace("  ", " ").Replace("\"\"", null);
                            itemAsString = "\"" + itemAsString + "\"";
                            result.Append(itemAsString + delimiter).Replace("\"\"", null);

                        }

                    }

                    result.Remove(--result.Length, 0);
                    result.Append(Environment.NewLine);

                }
                string datetimeformatted = DateTime.Now.ToString().Replace('/', '-').Replace(':', '-').Replace(' ', '-');
                filename = Credentials.csvRoot + "straydata-" + datetimeformatted + ".csv";
                using (StreamWriter writer = new StreamWriter(filename))
                {
                    writer.Write(result.ToString());

                }
            }

            catch (Exception error)
            {
                SendMeExceptionError(error);
            }
        }

      static void ImageWriterEngine(string animalID)
	  //Selects the image data from the photo view and writes it to an image directory
        {
            try
            {
                SqlConnection con = new SqlConnection(Credentials.connectionString);
                con.Open();

                SqlDataAdapter imageID = new SqlDataAdapter("select image_data from sysadm.v_photo where image_id = '" + animalID + "'", con);
                DataSet animalPic = new DataSet();
                imageID.Fill(animalPic);

                Byte[] data = new Byte[0];
                data = (Byte[])(animalPic.Tables[0].Rows[0]["image_data"]);
                MemoryStream memStream1 = new MemoryStream(data);
                Bitmap bmp = new Bitmap(Image.FromStream(memStream1));
                bmp.Save(Credentials.imageDir + animalID + ".jpg");
                con.Close();
            }
            catch (Exception error)
            {
                SendMeExceptionError(error);
            }
        }

      static void ImageWriterExecutor()
	 //Find new animals, or new pictures of animals who already are up on StrayMapper
        {
            try
            {
                SqlConnection con = new SqlConnection(Credentials.connectionString);
                con.Open();

                DataTable imagesTable = new DataTable();
                SqlDataAdapter imagesAdapter = new SqlDataAdapter

                                        (@"with kitten  as (select ROW_NUMBER() OVER ( PARTITION BY image_id order by image_seq DESC) as 'RowNumber',
                    image_id, image_seq
                    from sysadm.picture_it where image_id is not null and image_resolution = 'Detail')

                    select ki.image_id, ki.image_seq from kitten ki
                    left join sysadm.straymapper_image si
                    on ki.image_id = si.image_id
                    where RowNumber = 1
                    and ki.image_id in
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
			                    and k.intake_cond != 'DEAD')
                    and 
                    (not (ki.image_id in
                    (select image_id from straymapper_image))
                    or
                    ki.image_id in (select straymapper_image.image_id from straymapper_image 
                    inner join kitten
                    on kitten.image_id = straymapper_image.image_id
                    where kitten.image_seq > straymapper_image.image_seq))", con);

                imagesAdapter.Fill(imagesTable);

                for (int i = 0; i < imagesTable.Rows.Count; i++)
                {
                    string animalID2 = imagesTable.Rows[i][0].ToString();
                    ImageWriterEngine(animalID2);
                }
                con.Close();
            }

            catch (Exception error)
            {
                SendMeExceptionError(error);
            }
        }

      static void StrayMapperImageUploader()
	  //Put 'em in the cloud
        {
            try
            {

                System.IO.DirectoryInfo localStrayMapperImageDirectory = new DirectoryInfo(Credentials.imageDir);
                foreach (FileInfo imageFile in localStrayMapperImageDirectory.GetFiles())
                {
                    var request = new PutObjectRequest()
                        .WithBucketName(Credentials.bucketName)
                        .WithCannedACL(S3CannedACL.PublicRead)
                        .WithFilePath(imageFile.FullName)
                        .WithKey("images/" + imageFile.Name);
                    //the key will need to be modified to the key/faux-directory you're keeping images in on your hosting client

                    AmazonS3Client strayMapper = new AmazonS3Client(Credentials.accessKey, Credentials.secretAccessKey);

                    using (var upload = strayMapper.PutObject(request)) { }
                }
            }

            catch (Exception error)
            {
                SendMeExceptionError(error);
            }
        }

      static void ImageTrackerUpdate()
	  //updates straymapper_image with the most recent status
        {
            try
            {
                SqlConnection con = new SqlConnection(Credentials.connectionString);
                con.Open();

                using (SqlCommand updateTable = new SqlCommand())
                {
                    updateTable.Connection = con;
                    updateTable.CommandText = "delete from straymapper_image;";
                    updateTable.ExecuteNonQuery();
                    updateTable.CommandText = @"with kitten as (select ROW_NUMBER() OVER ( PARTITION BY image_id order by image_seq DESC) as 'RowNumber',
                                        image_id, image_seq
                                        from sysadm.picture_it where image_id is not null and image_resolution = 'Detail')

                                        insert into straymapper_image(image_id, image_seq)

                                        select image_id, image_seq from kitten
                                        where RowNumber = 1
                                        and image_id in
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
			                                        and k.intake_cond != 'DEAD')";
                    updateTable.ExecuteNonQuery();
                }
                con.Close();
            }

            catch (Exception error)
            {
                SendMeExceptionError(error);
            }
        }

      static void SendMeExceptionError(Exception error)
	  //just a method to e-mail yourself any exception errors
	  //if you remove this, you may want to add finally blocks to the other methods
	  //to ensure the program exits on an exception that you haven't handled
        {
            try
            {
                DirectoryInfo DI = new DirectoryInfo(Credentials.baseDirectory);

                foreach (FileInfo myFileInfo in DI.GetFiles())
                {
                    if (myFileInfo.FullName == Credentials.baseDirectory + "exception.txt")
                    {
                        myFileInfo.Delete();
                    }

                }

                using (StreamWriter writer = new StreamWriter(Credentials.baseDirectory + "exception.txt"))
                {
                    writer.Write(error.ToString());
                }

                using (MailMessage exceptionError = new MailMessage())
                {
                    MailAddress recipient = new MailAddress(Credentials.fromAddress);
                    MailAddress me = new MailAddress(Credentials.fromAddress);
                    Attachment exceptionFile = new Attachment(Credentials.baseDirectory + "exception.txt");
                    exceptionError.To.Add(recipient);
                    exceptionError.From = me;
                    exceptionError.Subject = "StrayMapper Exception Error " + DateTime.Now.ToString("D");
                    exceptionError.Attachments.Add(exceptionFile);


                    using (SmtpClient myServer = new SmtpClient(Credentials.emailServer, Credentials.port))
                    {
                        myServer.Credentials = System.Net.CredentialCache.DefaultNetworkCredentials;
                        myServer.Send(exceptionError);
                    }
                }
            }

            finally
            {
                
            }

        }

      static void SendCSVFile()
	  //emails it to the webhook
        {
            try
            {
                string datetimeformatted = DateTime.Now.ToString().Replace('/', '-').Replace(':', '-').Replace(' ', '-');

                using (MailMessage cityPetzMailGun = new MailMessage())
                {
                    MailAddress recipient = new MailAddress(Credentials.webhookEmail);
                    MailAddress me = new MailAddress(Credentials.fromAddress);
                    Attachment csvFile = new Attachment(filename);

                    cityPetzMailGun.To.Add(recipient);
                    cityPetzMailGun.From = me;
                    cityPetzMailGun.Subject = "Data for " + DateTime.Now.ToString("D");
                    cityPetzMailGun.Body = "Message intentionally not left blank.";
                    cityPetzMailGun.Attachments.Add(csvFile);

                    using (SmtpClient myServer = new SmtpClient(Credentials.emailServer, Credentials.port))
                    {
                        myServer.Credentials = System.Net.CredentialCache.DefaultNetworkCredentials;
                        myServer.Send(cityPetzMailGun);
                    }
                }
            }

            catch (Exception error)
            {
                SendMeExceptionError(error);
            }
        }

      static void DirectoryClearer()
	  //clears the stuff out to make way for updated data
        {
            try
            {
                System.IO.DirectoryInfo localStrayMapperImageDirectory = new DirectoryInfo(Credentials.imageDir);

                foreach (FileInfo imageFile in localStrayMapperImageDirectory.GetFiles())
                {
                    imageFile.Delete();
                }

                DirectoryInfo csvLocation = new DirectoryInfo(Credentials.csvRoot);

                foreach (FileInfo csvFile in csvLocation.GetFiles())
                {

                    csvFile.Delete();
                }

            }

            catch (Exception error)
            {
                SendMeExceptionError(error);
            }
        }
    }
}
