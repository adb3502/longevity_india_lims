package com.krishagni.catissueplus.core.biospecimen.domain;

import java.util.Date;

import com.krishagni.catissueplus.core.administrative.domain.User;

public class BharatParticipant {
    private Long id;
    
    private Participant participant;
    
    private String centerCode;
    
    private Integer ageGroup;
    
    private String gender; // A=Male, B=Female
    
    private Integer sequentialNumber;
    
    private String fullCode; // e.g., RAM-1A-001
    
    private String enrollmentStatus;
    
    private Date enrollmentDate;
    
    private User createdBy;
    
    private Date createdDate;
    
    private User lastUpdatedBy;
    
    private Date lastUpdatedDate;
    
    public Long getId() {
        return id;
    }
    
    public void setId(Long id) {
        this.id = id;
    }
    
    public Participant getParticipant() {
        return participant;
    }
    
    public void setParticipant(Participant participant) {
        this.participant = participant;
    }
    
    public String getCenterCode() {
        return centerCode;
    }
    
    public void setCenterCode(String centerCode) {
        this.centerCode = centerCode;
    }
    
    public Integer getAgeGroup() {
        return ageGroup;
    }
    
    public void setAgeGroup(Integer ageGroup) {
        this.ageGroup = ageGroup;
    }
    
    public String getGender() {
        return gender;
    }
    
    public void setGender(String gender) {
        this.gender = gender;
    }
    
    public Integer getSequentialNumber() {
        return sequentialNumber;
    }
    
    public void setSequentialNumber(Integer sequentialNumber) {
        this.sequentialNumber = sequentialNumber;
    }
    
    public String getFullCode() {
        return fullCode;
    }
    
    public void setFullCode(String fullCode) {
        this.fullCode = fullCode;
    }
    
    public String getEnrollmentStatus() {
        return enrollmentStatus;
    }
    
    public void setEnrollmentStatus(String enrollmentStatus) {
        this.enrollmentStatus = enrollmentStatus;
    }
    
    public Date getEnrollmentDate() {
        return enrollmentDate;
    }
    
    public void setEnrollmentDate(Date enrollmentDate) {
        this.enrollmentDate = enrollmentDate;
    }
    
    public User getCreatedBy() {
        return createdBy;
    }
    
    public void setCreatedBy(User createdBy) {
        this.createdBy = createdBy;
    }
    
    public Date getCreatedDate() {
        return createdDate;
    }
    
    public void setCreatedDate(Date createdDate) {
        this.createdDate = createdDate;
    }
    
    public User getLastUpdatedBy() {
        return lastUpdatedBy;
    }
    
    public void setLastUpdatedBy(User lastUpdatedBy) {
        this.lastUpdatedBy = lastUpdatedBy;
    }
    
    public Date getLastUpdatedDate() {
        return lastUpdatedDate;
    }
    
    public void setLastUpdatedDate(Date lastUpdatedDate) {
        this.lastUpdatedDate = lastUpdatedDate;
    }
    
    /**
     * Generate the participant code based on center, age group, gender, and sequential number
     */
    public void generateCode() {
        if (centerCode != null && ageGroup != null && gender != null && sequentialNumber != null) {
            this.fullCode = String.format("%s-%d%s-%03d", 
                centerCode, 
                ageGroup, 
                gender, 
                sequentialNumber);
        }
    }
    
    /**
     * Get the visual coding information for labels
     * @return Object containing cryocap color and label border color
     */
    public VisualCoding getVisualCoding() {
        VisualCoding coding = new VisualCoding();
        
        // Cryocap colors by age group
        switch (ageGroup) {
            case 1:
                coding.setCryocapColor("Blue");
                break;
            case 2:
                coding.setCryocapColor("Green");
                break;
            case 3:
                coding.setCryocapColor("Yellow");
                break;
            case 4:
                coding.setCryocapColor("Orange");
                break;
            case 5:
                coding.setCryocapColor("Red");
                break;
        }
        
        // Label border colors by gender
        if ("A".equals(gender)) {
            coding.setLabelBorderColor("Blue");
        } else if ("B".equals(gender)) {
            coding.setLabelBorderColor("Pink");
        }
        
        return coding;
    }
    
    public static class VisualCoding {
        private String cryocapColor;
        private String labelBorderColor;
        
        public String getCryocapColor() {
            return cryocapColor;
        }
        
        public void setCryocapColor(String cryocapColor) {
            this.cryocapColor = cryocapColor;
        }
        
        public String getLabelBorderColor() {
            return labelBorderColor;
        }
        
        public void setLabelBorderColor(String labelBorderColor) {
            this.labelBorderColor = labelBorderColor;
        }
    }
}