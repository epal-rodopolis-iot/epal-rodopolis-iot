# Ένα πλήρως ολοκληρωμένο σύστημα Internet of Things

# Σύντομη περιγραφή

Σκοπός του project είναι η δημιουργία ενός πρωτοτύπου συστήματος πραγματικού χρόνου που θα παρακολουθεί, με τη χρήση μικροϋπολογιστή (**Raspberry  Pi**) και αισθητήρων, τις παραμέτρους του περιβάλλοντος χώρου που θα επιλέγουμε (ενδεικτικά θερμοκρασία, υγρασία, κοκ). Το σύστημα αυτό θα μεταδίδει δεδομένα αλλά και θα δέχεται πληροφορίες και εντολές προς/και από τη διαδικτυακή πλατφόρμα της **[Amazon (AWS)](https://aws.amazon.com/)**.  Για την near - real - time καταγραφή και προβολή των τιμών που μετρούν οι αισθητήρες στο Internet, θα γίνει χρήση της πλατφόρμας **[ThingSpeak](https://thingspeak.com/)**  της **[MathWorks](https://www.mathworks.com/)**. Η ίδια πλατφόρμα θα χρησιμοποιηθεί και για την επεξεργασία των τιμών με την χρήση της γλώσσας Matlab. Το σύνολο των τεχνολογιών που θα χρησιμοποιηθούν είναι ανοικτές.


# Αναλυτική περιγραφή

Το συνολικό σύστημα (Rapsberry PI - Αισθητήρες – AWS - ThingSpeak) θα μπορεί:

- Να καταγράφει τις παραμέτρους που επιθυμούμε και να τις προωθεί στο Internet μέσω του **HTTP** και με τη χρήση του αντίστοιχου **REST API** αναλόγως της πλατφόρμας που οι τιμές θα καταλήγουν (**[AWS](https://aws.amazon.com/)** ή **[MathWorks](https://www.mathworks.com/)**).

- 	Να αποστέλλει μηνύματα (email – SMS) σε περίπτωση υπέρβασης των ορίων των τιμών που μετράμε (με την χρήση της rule based πλατφόρμας **[AWS SNS](https://aws.amazon.com/sns/)**,  της ειδικής **[SQLγια ΙΟΤ](https://docs.aws.amazon.com/iot/latest/developerguide/iot-sql-reference.html)** εφαρμογές, και τον προγραμματισμό με **[Python](https://www.python.org/)** του **[serverless computing](https://aws.amazon.com/lambda/)** περιβάλλοντος της **[Amazon – Lambda](https://aws.amazon.com/lambda/)**). Συνάμα θα γίνει και ολοκλήρωση του συστήματος AWS Lambda με το σύστημα αποστολής SMS που λειτουργεί στο ΕΠΑΛ Ροδόπολης το οποίο και είναι πλήρως ανοιχτό (πληροφορίες στο https://github.com/chertouras/myschoolsms_V2.0 ) 


-	Να ελέγχει τις συνδεδεμένες στο [Raspberry PI](https://www.raspberrypi.org/) συσκευές (π.χ dc μοτερ) μέσω της χρήσης του πρωτοκόλλου [MQTT](http://mqtt.org/), των [AWS  IOT Device Shadows](https://docs.aws.amazon.com/iot/latest/developerguide/iot-device-shadows.html) και του message broker τους, της γλώσσας Python καθώς και του [AWS Python SDK](https://aws.amazon.com/sdk-for-python/).  

~~-	Να δέχεται εντολές από ένα [IOT Button](https://aws.amazon.com/iotbutton/) για τη διαπεραίωση απλών καθηκόντων απο το Raspberry Pi, όπως το άνοιγμα και το κλείσιμο ενός μοτέρ ή ενός led, με σκοπό την τροποποίηση των παραμέτρων του περιβάλλοντος (π.χ. εκκίνηση ενός ανεμιστήρα για την πτώση της θερμοκρασίας, άνοιγμα ενός led για φωτισμό κοκ).~~ Το σύστημα δεν υλοποιήθηκε λόγω έλλειψης χρηματοδότησης.

- Να δέχεται φωνητικές εντολές τις οποίες θα ερμηνεύει και θα εκτελεί μέσω ενός **[VUI (Voice User Interface)](https://developer.amazon.com/alexa-skills-kit/vui)** και της συσκευής [Echo Dot](https://www.amazon.com/Amazon-Echo-Dot-Portable-Bluetooth-Speaker-with-Alexa-Black/dp/B01DFKC2SO).
Οι εν λόγω εντολές θα εκτελούνται μέσω της προγραμματιστικής διασύνδεσης του service της ALEXA, του Raspberry Pi και των AWS Lambda functions. 

# Λίστα υλικών

Για την υλοποίηση του συστήματος απαιτούνται: 

- Ένα Raspberry Pi 3 Β+ πλήρες κιτ με όλα του τα παρελκόμενα (τροφοδοσία , ψύκτρα , λειτουργικό σε microSD , USB stick adapter κλπ)
- Ένα Amazon ΙΟΤ button.
- Μια συσκευή Amazon Echo Dot (second/third generation) ή μια συσκευή Amazon Alexa.
- Αισθητήρες περιβάλλοντος (DHT 22 και ΒΜP280).
- Δυο breadboard και ένα πλήρες σετ καλωδίων M/F , F/M , M/M για τη διασύνδεση των GPIO ports.
- Ένα Assembled Pi T-Cobbler Plus - GPIO Breakout. 
- Αντιστάσεις, led και καλώδια breadboard.
- Μια οθόνη LCD > 19’’ με HDMI έξοδο για την σύνδεση του Raspberry PI.
- Πληκτρολόγιο και ποντίκι USB.
- Δυο Character LCD (16X2 LCD Display) για προβολή πληροφοριών στο breadboard.
- Ένα απλό μοτέρ hobby 3.3V ή 5V
- Ενα shield ελέγχου μοτερ ( L293D ή παρόμοια με διαθέσιμο python api).
- Ένα εργαστηριακό τροφοδοτικό μεταβλητής τάσης 0-18V και 0-3A για το breadboard με LCD οθόνη ένδειξης τάσης και τα αντίστοιχα καλώδια για σύνδεση με το breadboard

######   Το κόστος χρήσης των AWS θα βαρύνει το υπεύθυνο της ομάδας κατά την διάρκεια του διαγωνισμού. 
