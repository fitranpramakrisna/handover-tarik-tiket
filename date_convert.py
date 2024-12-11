def date_eng_to_indo(hari_inggris):
      hari_indonesia = {
      "Sunday": "Minggu",
      "Monday": "Senin",
      "Tuesday": "Selasa",
      "Wednesday": "Rabu",
      "Thursday": "Kamis",
      "Friday": "Jumat",
      "Saturday": "Sabtu"
  }
      if hari_inggris in hari_indonesia:
          return hari_indonesia[hari_inggris]