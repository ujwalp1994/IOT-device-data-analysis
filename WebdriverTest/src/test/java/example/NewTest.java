package example;		

import org.testng.annotations.Test;
import org.testng.AssertJUnit;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

import org.openqa.selenium.By;		
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.remote.DesiredCapabilities;
import org.openqa.selenium.remote.RemoteWebDriver;
import org.testng.Assert;		
import org.testng.annotations.Test;	
import org.testng.annotations.BeforeTest;	
import org.testng.annotations.AfterTest;		
public class NewTest {		
	    public WebDriver driver;
	    public static final String URL = "http://0.0.0.0:4444/wd/hub";
		public static boolean flag=false;
		@Test				
		public void testEasy() throws InterruptedException, IOException {	
			System.out.println("Session started...");
		    driver.get("https://my.hexoskin.com/en/login");
		    driver.findElement(By.id("login_username")).sendKeys("shalwak@gmail.com");
		    driver.findElement(By.id("password")).sendKeys("123456");
		    driver.findElement(By.id("submit-button")).click();
		    driver.findElement(By.xpath("//*[@id=\"wrap\"]/div[1]/div/div/div/ul[1]/li[4]/a")).click();
		    
		    List <WebElement> elements= driver.findElements(By.className("event"));
		    List<String> records = new ArrayList<String>();
		    List<String> check = new ArrayList<String>();
		    Thread.sleep(5000);
		    
		    Scanner s = new Scanner(new File("/record_data.txt"));
		    while(s.hasNext()) {
		    	check.add(s.next());
		    }
		    System.out.println("Reading file data...");
		    for(String c : check) {
		    	System.out.println(c);
		    }
		    
		   
		   for(WebElement ele : elements) {
			   records.add(ele.getAttribute("id"));
		   }
		   for(String rec : records) {
			   if(check.contains(rec)) {flag=true;}
			   else {
				   flag=false;
				   System.out.println("Adding file with record ID="+rec);
				   check.add(rec);
				   driver.findElement(By.xpath("//*[@id=\""+rec+"\"]/div/a")).click();
				   Thread.sleep(8000);
				   driver.findElement(By.cssSelector("#highcharts-0 > svg > g:nth-child(6)")).click();
				    
				   Thread.sleep(2000);
				   driver.findElement(By.xpath("//*[@id=\"highcharts-0\"]/div[2]/div/div[6]")).click();
				   System.out.println(driver.getTitle());
				    
				   Thread.sleep(5000);
				    
				   driver.navigate().back();
				   Thread.sleep(8000);
			   }
		   }
		   
		   if(flag==true) {
			   System.out.println("Nothin to fetch!!");
		   }
		   
		   FileWriter writer = new FileWriter("/Users/ujwal/eclipse-workspace/Selenium/src/record_data.txt"); 
		   for(String str: check) {
		     writer.write(str+System.getProperty("line.separator"));
		   }
		   writer.close();		
		  }	
		
		@BeforeTest
		public void beforeTest() throws MalformedURLException {	
			DesiredCapabilities cp = new DesiredCapabilities();
			cp.setCapability("browser", "Chrome");
		    driver = new RemoteWebDriver(new URL(URL), cp);  
		}		
		@AfterTest
		public void afterTest() {
			driver.quit();			
		}		
}	
