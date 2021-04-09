---
title: Chamber of Secrets 
---
---

Built on the principles of *Ethical Data*, **Chamber of Secrets** is a redefined Digital Locker system straight out of the magical Harry Potter universe created by J.K. Rowling. Inspired by the *One-Who-Must-Not-Be-Named*, Lord Voldermort himself, we ensure that your data is accessible to you, and **only you**. 

:::note

**Chamber of Secrets doesn't store your Data!** Your data is stored on your Google Drive and Dropbox storages. We just add layers of security to the data in a way that even if your accounts get compromized, there's no way a hacker can access your files!

:::

## How Does It Work?
---

Remember how **Lord Voldermort** splits his soul into 7 **Horcruxes** in an attempt to make himself immortal? That concept struck a chord in our minds.  

"What if we split a file into 3 parts and just spread it over the internet?"

This was the question that ultimately led to the final product— Chamber of Secrets.

### Here's how Chamber of Secrets works:

1. The user signs up for our platform, that is free of cost since the project is open sourced.

![Signup Screen](/img/signup.jpg)

2. Upon signing up, they get a unique Private Key.

![Private Key Screen](/img/private.jpg) 
 
:::warning Take Care

We don't store the private key of the user! It is made available to the user to copy/download just once at the time of account creation. 

**KEEP THE KEY SAFE AND SUCH THAT NO ONE ELSE OTHER THAN YOU CAN ACCESS IT!**

If the key is lost, all the encrypted, uploaded files can NEVER be decrypted again and will be lost forever. 

:::

3. The user downloads and stored the private key safely.
4. Next they are taken to the OAuth screen where they need to authenticate into both their **Google Drive** and **Dropbox** accounts. 

![OAuth Screen](/img/oauth.jpg)

5. Once done, they are finally taken to the locker screen. Here's where they can upload their files, download (if any), or delete their files.

![Home Screen](/img/home.jpg) 

#### Seems pretty simple and user-friendly, right? 

Well, the backend is where all the magic happens!

### User Uploads a File:

To upload a file, the user clicks on **Upload New File**. User selects a file, enters their private key and hits upload.

![Upload](/img/upload.jpg) 

Now behind the scene, the file gets encrypted, split into 3 "Horcruxes", then these Horcruxes get uploaded on the user's Google Drive and Dropbox. 

:::info

**Let's say someone wants to access the files that you uploaded**. Now, to do that, they'll be needing either of the 2 combinations:

1. Your Chamber of Secrets account credentials, and your private key.
2. Access to our backend database *(for file IDs and user's public key)*, credentials to your Google Drive account, credentials to your Dropbox account, and your private key.

If they don't have all these, your files are **virtually un-crackable**! You **cannot** decrypt a single horcrux and, say, access 1/3<sup>rd</sup> of the data. To get the original file, all the 3 Horcruxes are required!

:::


### User Downloads a File:

To download a file, the user has to double-click on the file. Then, once they enter their private key, they hit download button.
 
![Download](/img/download.jpg)

Behind the scenes, the individual, encrypted Horcruxes get downloaded from user's file storage services, get re-combined into an encrypted file, and then get decrypted before getting returned back to the user. 

Sounds pretty cool, right?

### User Deletes a File:

For deleting a file, user needs to just select the file by doing a single-click, then hit delete. It's that easy!

![Delete](/img/delete.jpg) 

Behing the scenes, the Horcruxes get wiped from the user's file storage and all the records get deleted from the database. 

    "Evanesco!"

     — Hermione Granger

## Security and Additional Features
---

These are the security features provided by Chamber of Secrets:

#### Hybrid Encryption
Chamber of Secrets uses a combination of symmetric and asymmetric encryption. Upon signup, we generate a pair of public and private key for the user. We encrypt the public key with the private key, and store it in our database, and send the private key to the user WITHOUT saving it. Now, the encryption and decryption is done with the public key, that has to first be decrypted itseld using the private key that the user has to enter at the time of file uploads and file downloads.

#### Multi-Layered Security
Once a file gets split and encrypted, it is virtually impossible for anyone to break into, unless they have access to our database, user's private key, and all the horcruxes which by the way get stored anonymously on the user's Google Drive and Dropbox WITHOUT any metadata or identification of any sorts. 

:::info

As a user, if I check my Google Drive or Dropbox, I myself won't be able to identify what file the horcrux belongs to, which adds to an additional layer of security because the file can only be decrypted if the horcruxes are arranged in the correct order before re-combining.

:::

#### Zero Cost
We are using existing platforms for file storage that are free to use and the user generally already has— Google Drive, Dropbox and soon OneDrive too. So the user won't have to pay any additional cost (say, gas or storage fee on a blockchain-based storage like IPFS).

#### Data-Leak Proof
:::note

Chamber of Secrets is **100% DATA-LEAK PROOF**!

:::

Say our database gets hacked! Well no worries. No one can access your data as long as you still have your private key "private".

Your Google Drive and Dropbox passwords are compromized? Again, no worries because your horcruxes are encrypted and can only be decrypted once the intruder has your private key, public key, and knows the correct order to arrange the horcruxes in.

If we talk in terms of probability, the chances of all your accounts, your private key, and our database getting compromised all at the same time is next to nothing. We know how to preserve your "*Secrets*".